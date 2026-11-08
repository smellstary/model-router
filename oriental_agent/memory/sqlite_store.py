"""
记忆的 SQLite 试点。

承接 MemorySystem.store / associate / retrieve 用到的节点、干支标签和关联。
未设置路径时 MemorySystem 仍只在内存里，已有调用不用改。
对话内核在 core.agent 里默认把这一条路径接到 data/agent_memory.sqlite。
旧库缺列时会补列，不要求删掉已有文件。
"""

import importlib
import json
import os
import sqlite3
import threading
from datetime import datetime
from typing import Any, Callable, List, Optional, Tuple

from core.types import MemoryAssociation, MemoryLayer, MemoryNode, WuxingType


def _member_name(value: Any) -> str:
    """取枚举成员名。预测卦象把 _name_ 覆写成卦名，不能用 .name。"""
    enum_cls = type(value)
    for member_name, member in getattr(enum_cls, "__members__", {}).items():
        if member is value:
            return member_name
    return str(getattr(value, "name", value))


def _enum_token(value: Any) -> str:
    return f"{value.__class__.__module__}:{value.__class__.__name__}:{_member_name(value)}"


def _enum_from_token(token: str) -> Any:
    module_name, class_name, member = token.split(":", 2)
    enum_cls = getattr(importlib.import_module(module_name), class_name)
    try:
        return enum_cls[member]
    except KeyError:
        for item in enum_cls:
            if _member_name(item) == member:
                return item
            if getattr(item, "name", None) == member:
                return item
            item_value = getattr(item, "value", None)
            if item_value == member or (isinstance(item_value, tuple) and member in item_value):
                return item
        raise


def _optional_enum_token(value: Any) -> Optional[str]:
    if value is None:
        return None
    return _enum_token(value)


def _optional_enum_from_token(token: Optional[str]) -> Any:
    if not token:
        return None
    return _enum_from_token(token)


class SqliteMemoryStore:
    """把记忆节点写入单个 SQLite 文件，并在打开时整表读回。

    每个线程单独打开连接。跨进程并发写依赖 WAL、busy_timeout 和 IMMEDIATE 事务。
    """

    def __init__(self, path: str):
        directory = os.path.dirname(os.path.abspath(path))
        if directory:
            os.makedirs(directory, exist_ok=True)
        self.path = path
        self._local = threading.local()
        connection = self._connection()
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (
                memory_id TEXT PRIMARY KEY,
                content_json TEXT NOT NULL,
                memory_type TEXT NOT NULL,
                layer TEXT NOT NULL,
                wuxing TEXT NOT NULL,
                strength REAL NOT NULL,
                weight REAL NOT NULL,
                yin_yang_balance REAL NOT NULL,
                created_at TEXT NOT NULL,
                last_accessed TEXT NOT NULL,
                context_json TEXT NOT NULL,
                tiangan TEXT,
                dizhi TEXT,
                associations_json TEXT NOT NULL DEFAULT '[]'
            )
            """
        )
        self._connection().execute(
            """
            CREATE TABLE IF NOT EXISTS associations (
                source_id TEXT NOT NULL,
                target_id TEXT NOT NULL,
                association_type TEXT NOT NULL,
                wuxing_relationship TEXT NOT NULL,
                strength REAL NOT NULL,
                bidirectional INTEGER NOT NULL,
                PRIMARY KEY (source_id, target_id, association_type)
            )
            """
        )
        self._migrate()
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS hexagram_transitions (
                from_token TEXT NOT NULL,
                to_token TEXT NOT NULL,
                count INTEGER NOT NULL,
                probability REAL NOT NULL,
                PRIMARY KEY (from_token, to_token)
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS memory_revision (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                revision INTEGER NOT NULL
            )
            """
        )
        connection.execute(
            "INSERT OR IGNORE INTO memory_revision (id, revision) VALUES (1, 0)"
        )
        connection.commit()

    def _connection(self) -> sqlite3.Connection:
        """当前线程的连接。fork 之后的子进程必须自己 new 一个 store，不要复用父进程连接。"""
        connection = getattr(self._local, "conn", None)
        if connection is None:
            connection = sqlite3.connect(self.path, timeout=5.0, check_same_thread=True)
            connection.row_factory = sqlite3.Row
            connection.execute("PRAGMA journal_mode=WAL")
            connection.execute("PRAGMA synchronous=NORMAL")
            connection.execute("PRAGMA busy_timeout=5000")
            self._local.conn = connection
        return connection

    def _write(self, work: Callable[[sqlite3.Connection], None]) -> None:
        """IMMEDIATE 事务里写，并递增修订号。别的进程靠这个号丢掉过期内存索引。"""
        connection = self._connection()
        try:
            connection.execute("BEGIN IMMEDIATE")
            work(connection)
            connection.execute(
                "UPDATE memory_revision SET revision = revision + 1 WHERE id = 1"
            )
            connection.commit()
        except Exception:
            connection.rollback()
            raise

    def revision(self) -> int:
        row = self._connection().execute(
            "SELECT revision FROM memory_revision WHERE id = 1"
        ).fetchone()
        return int(row["revision"]) if row else 0

    def _migrate(self) -> None:
        """给 P2 建出来的旧表补上干支和关联列。"""
        columns = {
            row["name"]
            for row in self._connection().execute("PRAGMA table_info(memories)")
        }
        if "tiangan" not in columns:
            self._connection().execute("ALTER TABLE memories ADD COLUMN tiangan TEXT")
        if "dizhi" not in columns:
            self._connection().execute("ALTER TABLE memories ADD COLUMN dizhi TEXT")
        if "associations_json" not in columns:
            self._connection().execute(
                "ALTER TABLE memories ADD COLUMN associations_json TEXT NOT NULL DEFAULT '[]'"
            )

    def close(self) -> None:
        connection = getattr(self._local, "conn", None)
        if connection is not None:
            connection.close()
            self._local.conn = None

    def upsert(self, memory: MemoryNode) -> None:
        def work(connection: sqlite3.Connection) -> None:
            connection.execute(
            """
            INSERT INTO memories (
                memory_id, content_json, memory_type, layer, wuxing,
                strength, weight, yin_yang_balance, created_at, last_accessed, context_json,
                tiangan, dizhi, associations_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(memory_id) DO UPDATE SET
                content_json = excluded.content_json,
                memory_type = excluded.memory_type,
                layer = excluded.layer,
                wuxing = excluded.wuxing,
                strength = excluded.strength,
                weight = excluded.weight,
                yin_yang_balance = excluded.yin_yang_balance,
                created_at = excluded.created_at,
                last_accessed = excluded.last_accessed,
                context_json = excluded.context_json,
                tiangan = excluded.tiangan,
                dizhi = excluded.dizhi,
                associations_json = excluded.associations_json
            """,
            (
                memory.memory_id,
                json.dumps(memory.content, ensure_ascii=False, default=str),
                _enum_token(memory.memory_type),
                _enum_token(memory.layer),
                _enum_token(memory.wuxing_attribute),
                float(memory.strength),
                float(memory.weight),
                float(memory.yin_yang_balance),
                memory.created_at.isoformat(),
                memory.last_accessed.isoformat(),
                json.dumps(memory.context or {}, ensure_ascii=False, default=str),
                _optional_enum_token(memory.tiangan_tag),
                _optional_enum_token(memory.dizhi_tag),
                json.dumps(list(memory.associations or []), ensure_ascii=False),
            ),
            )
        self._write(work)

    def save_association(self, association: MemoryAssociation) -> None:
        def work(connection: sqlite3.Connection) -> None:
            connection.execute(
            """
            INSERT INTO associations (
                source_id, target_id, association_type, wuxing_relationship,
                strength, bidirectional
            ) VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(source_id, target_id, association_type) DO UPDATE SET
                wuxing_relationship = excluded.wuxing_relationship,
                strength = excluded.strength,
                bidirectional = excluded.bidirectional
            """,
            (
                association.source_id,
                association.target_id,
                _enum_token(association.association_type),
                _enum_token(association.wuxing_relationship),
                float(association.strength),
                1 if association.bidirectional else 0,
            ),
            )
        self._write(work)

    def update_strengths(self, pairs: List[tuple]) -> None:
        """只更新强度，不改 last_accessed。一次事务提交。"""
        if not pairs:
            return

        def work(connection: sqlite3.Connection) -> None:
            connection.executemany(
                "UPDATE memories SET strength = ? WHERE memory_id = ?",
                [(float(strength), memory_id) for memory_id, strength in pairs],
            )

        self._write(work)

    def delete(self, memory_id: str) -> None:
        def work(connection: sqlite3.Connection) -> None:
            connection.execute("DELETE FROM memories WHERE memory_id = ?", (memory_id,))
            connection.execute(
                "DELETE FROM associations WHERE source_id = ? OR target_id = ?",
                (memory_id, memory_id),
            )

        self._write(work)

    def save_transitions(self, rows: List[Tuple[str, str, int, float]]) -> None:
        """整表替换八卦转移计数。空列表表示回到尚未观察的状态。"""
        def work(connection: sqlite3.Connection) -> None:
            connection.execute("DELETE FROM hexagram_transitions")
            connection.executemany(
                """
                INSERT INTO hexagram_transitions (from_token, to_token, count, probability)
                VALUES (?, ?, ?, ?)
                """,
                rows,
            )

        self._write(work)

    def load_transitions(self) -> List[Tuple[str, str, int, float]]:
        rows = self._connection().execute(
            """
            SELECT from_token, to_token, count, probability
            FROM hexagram_transitions
            ORDER BY from_token, to_token
            """
        ).fetchall()
        return [
            (row["from_token"], row["to_token"], int(row["count"]), float(row["probability"]))
            for row in rows
        ]

    def load_all(self) -> List[MemoryNode]:
        rows = self._connection().execute(
            """
            SELECT memory_id, content_json, memory_type, layer, wuxing,
                   strength, weight, yin_yang_balance, created_at, last_accessed, context_json,
                   tiangan, dizhi, associations_json
            FROM memories
            ORDER BY created_at
            """
        ).fetchall()
        memories = []
        for row in rows:
            content = json.loads(row["content_json"])
            context = json.loads(row["context_json"]) if row["context_json"] else {}
            raw_links = row["associations_json"] or "[]"
            try:
                links = json.loads(raw_links)
            except json.JSONDecodeError:
                links = []
            wuxing = _enum_from_token(row["wuxing"])
            if not isinstance(wuxing, WuxingType):
                wuxing = WuxingType.EARTH
            layer = _enum_from_token(row["layer"])
            if not isinstance(layer, MemoryLayer):
                layer = MemoryLayer.HUMAN
            memories.append(MemoryNode(
                memory_id=row["memory_id"],
                content=content,
                memory_type=_enum_from_token(row["memory_type"]),
                layer=layer,
                yin_yang_balance=float(row["yin_yang_balance"]),
                wuxing_attribute=wuxing,
                tiangan_tag=_optional_enum_from_token(row["tiangan"]),
                dizhi_tag=_optional_enum_from_token(row["dizhi"]),
                weight=float(row["weight"]),
                strength=float(row["strength"]),
                created_at=datetime.fromisoformat(row["created_at"]),
                last_accessed=datetime.fromisoformat(row["last_accessed"]),
                associations=list(links) if isinstance(links, list) else [],
                context=context if isinstance(context, dict) else {},
            ))
        return memories

    def load_associations(self) -> List[MemoryAssociation]:
        rows = self._connection().execute(
            """
            SELECT source_id, target_id, association_type, wuxing_relationship,
                   strength, bidirectional
            FROM associations
            ORDER BY source_id, target_id
            """
        ).fetchall()
        return [
            MemoryAssociation(
                source_id=row["source_id"],
                target_id=row["target_id"],
                association_type=_enum_from_token(row["association_type"]),
                wuxing_relationship=_enum_from_token(row["wuxing_relationship"]),
                strength=float(row["strength"]),
                bidirectional=bool(row["bidirectional"]),
            )
            for row in rows
        ]
