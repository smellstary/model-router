"""SQLite 记忆试点：写入后换一个实例仍能按关键词找回。"""

import asyncio
import sqlite3

import pytest

from core.types import (
    AssociationType,
    DizhiType,
    HexagramType,
    MemoryLayer,
    MemoryQuery,
    QueryType,
    TianganType,
    WuxingType,
)
from memory.sqlite_store import SqliteMemoryStore
from memory.system import MemorySystem


def test_sqlite_store_and_retrieve_roundtrip(tmp_path):
    path = tmp_path / "agent_memory.sqlite"
    first = MemorySystem(persist_path=str(path))
    memory_id = asyncio.run(first.store(
        "投资10万的备忘",
        HexagramType.QIAN,
        MemoryLayer.HUMAN,
        context={"intent": "investment"},
    ))

    second = MemorySystem(persist_path=str(path))
    assert memory_id in second._memory_index
    found = asyncio.run(second.retrieve(MemoryQuery(
        query_type=QueryType.KEYWORD,
        keywords=["投资"],
    )))
    assert any(item.memory_id == memory_id for item in found)
    assert second._memory_index[memory_id].context["intent"] == "investment"


def test_wuxing_decay_is_written_back(tmp_path):
    path = tmp_path / "agent_memory.sqlite"
    system = MemorySystem(persist_path=str(path))
    memory_id = asyncio.run(system.store(
        "土性备忘",
        HexagramType.KUN,
        MemoryLayer.HUMAN,
    ))
    node = system._memory_index[memory_id]
    assert node.wuxing_attribute == WuxingType.EARTH
    node.strength = 1.0
    system._store.upsert(node)

    system.apply_wuxing_decay_step(active=WuxingType.WOOD, base_decay=0.05)

    reloaded = MemorySystem(persist_path=str(path))
    assert reloaded._memory_index[memory_id].strength == pytest.approx(0.925)


def test_tags_and_associations_survive_reload(tmp_path):
    path = tmp_path / "agent_memory.sqlite"
    first = MemorySystem(persist_path=str(path))
    left = asyncio.run(first.store(
        "甲项目投资备忘",
        HexagramType.QIAN,
        MemoryLayer.HUMAN,
        tiangan_tag=TianganType.JIA,
        dizhi_tag=DizhiType.ZI,
    ))
    right = asyncio.run(first.store(
        "乙项目现金流备忘",
        HexagramType.KUN,
        MemoryLayer.HUMAN,
    ))
    assert asyncio.run(first.associate(left, right, AssociationType.CAUSAL)) is True

    second = MemorySystem(persist_path=str(path))
    restored = second._memory_index[left]
    assert restored.tiangan_tag == TianganType.JIA
    assert restored.dizhi_tag == DizhiType.ZI
    assert right in restored.associations
    assert len(second._association_index) == 1
    found = asyncio.run(second.retrieve(MemoryQuery(
        query_type=QueryType.ASSOCIATION,
        keywords=["甲项目"],
    )))
    assert any(item.memory_id == right for item in found)


def test_old_sqlite_schema_gains_new_columns(tmp_path):
    path = tmp_path / "legacy.sqlite"
    connection = sqlite3.connect(path)
    connection.execute(
        """
        CREATE TABLE memories (
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
            context_json TEXT NOT NULL
        )
        """
    )
    connection.execute(
        """
        INSERT INTO memories VALUES (
            'mem_old', '"旧备忘"',
            'core.types:HexagramType:QIAN',
            'core.types:MemoryLayer:HUMAN',
            'core.types:WuxingType:EARTH',
            1.0, 1.0, 0.0,
            '2026-01-01T00:00:00', '2026-01-01T00:00:00',
            '{}'
        )
        """
    )
    connection.commit()
    connection.close()

    loaded = SqliteMemoryStore(str(path)).load_all()
    assert loaded[0].memory_id == "mem_old"
    assert loaded[0].content == "旧备忘"
    assert loaded[0].tiangan_tag is None
    assert loaded[0].associations == []


def test_dialog_process_memory_reopens(tmp_path, monkeypatch):
    monkeypatch.setenv("MEMORY_DB_PATH", str(tmp_path / "dialog.sqlite"))
    from core.agent import OrientalWisdomAgent

    first = OrientalWisdomAgent()
    response = asyncio.run(first.process("我想投资10万"))
    assert response.memory_updates

    second = OrientalWisdomAgent()
    found = asyncio.run(second.memory_system.retrieve(
        second._create_memory_query("投资")
    ))
    assert any("投资10万" in str(item.content) for item in found)


def test_dialog_hexagrams_can_be_associated(tmp_path):
    """对话内核存的是六十四卦，关联时不能因为转移矩阵只有八卦而崩溃。"""
    from prediction.prediction_engine import HexagramType as PredHex

    path = tmp_path / "hex.sqlite"
    system = MemorySystem(persist_path=str(path))
    left = asyncio.run(system.store("甲项目", PredHex.GUA_57, MemoryLayer.HUMAN))
    right = asyncio.run(system.store("乙项目", PredHex.GUA_11, MemoryLayer.HUMAN))
    assert asyncio.run(system.associate(left, right, AssociationType.SIMILAR)) is True

    reloaded = MemorySystem(persist_path=str(path))
    assert right in reloaded._memory_index[left].associations
    assert reloaded._memory_index[left].memory_type == PredHex.GUA_57


def test_memory_without_path_stays_in_process():
    system = MemorySystem()
    assert system._store is None
    memory_id = asyncio.run(system.store("只在内存", HexagramType.KAN, MemoryLayer.HUMAN))
    assert memory_id in system._memory_index
