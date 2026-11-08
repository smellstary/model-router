"""运行路径：短句不跑重子系统，投资缺现金流不报假 ROI，记忆有上限。"""

import asyncio
from datetime import datetime, timedelta

from config.settings import Config
from core.agent import OrientalWisdomAgent
from core.types import HexagramType, MemoryLayer, MemoryQuery, QueryType
from memory.system import MemorySystem


def test_hello_stays_on_the_light_path(monkeypatch):
    monkeypatch.setenv("MEMORY_DB_PATH", "")
    agent = OrientalWisdomAgent()
    response = asyncio.run(agent.process("你好"))
    assert response.state_changes["primary_intent"] == "hello"
    assert response.state_changes["light_path"] is True
    assert response.memory_updates == []
    assert "您好" in response.response_text
    assert "思考洞察" not in response.response_text


def test_investment_without_cashflow_does_not_quote_minus_100(monkeypatch):
    monkeypatch.setenv("MEMORY_DB_PATH", "")
    agent = OrientalWisdomAgent()
    response = asyncio.run(agent.process("我想投资10万"))
    assert response.state_changes["primary_intent"] == "investment"
    assert "数据不足" in response.response_text
    assert "ROI -100" not in response.response_text
    assert response.memory_updates


def test_memory_cap_drops_the_weakest(tmp_path):
    config = Config()
    config.set("memory.max_memories", 2)
    system = MemorySystem(config, persist_path=str(tmp_path / "cap.sqlite"))
    first = asyncio.run(system.store("第一条", HexagramType.QIAN, MemoryLayer.HUMAN))
    second = asyncio.run(system.store("第二条", HexagramType.KUN, MemoryLayer.HUMAN))
    system._memory_index[first].strength = 0.2
    system._store.upsert(system._memory_index[first])
    system._cached_revision = None
    third = asyncio.run(system.store("第三条", HexagramType.KAN, MemoryLayer.HUMAN))
    assert first not in system._memory_index
    assert second in system._memory_index
    assert third in system._memory_index
    reloaded = MemorySystem(config, persist_path=str(tmp_path / "cap.sqlite"))
    assert first not in reloaded._memory_index
    assert len(reloaded._memory_index) == 2


def test_retrieval_pool_ignores_older_weaker_rows():
    config = Config()
    config.set("memory.retrieval_pool", 1)
    system = MemorySystem(config)
    older = asyncio.run(system.store("独特甲备忘", HexagramType.QIAN, MemoryLayer.HUMAN))
    newer = asyncio.run(system.store("独特乙备忘", HexagramType.KUN, MemoryLayer.HUMAN))
    system._memory_index[older].last_accessed = datetime(2026, 1, 1)
    system._memory_index[newer].last_accessed = datetime(2026, 1, 1) + timedelta(days=1)
    found = asyncio.run(system.retrieve(MemoryQuery(
        query_type=QueryType.KEYWORD,
        keywords=["独特甲"],
    )))
    assert found == []
    kept = asyncio.run(system.retrieve(MemoryQuery(
        query_type=QueryType.KEYWORD,
        keywords=["独特乙"],
    )))
    assert kept and "独特乙" in str(kept[0].content)


def test_decay_does_not_refresh_last_accessed(tmp_path):
    system = MemorySystem(persist_path=str(tmp_path / "decay.sqlite"))
    memory_id = asyncio.run(system.store("土性备忘", HexagramType.KUN, MemoryLayer.HUMAN))
    seen = system._memory_index[memory_id].last_accessed
    system.apply_wuxing_decay_step(active=None, base_decay=0.05)
    reloaded = MemorySystem(persist_path=str(tmp_path / "decay.sqlite"))
    assert reloaded._memory_index[memory_id].last_accessed == seen
