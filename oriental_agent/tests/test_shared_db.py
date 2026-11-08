"""转移计数重启后一致；两个进程可以同时写同一个库。"""

import asyncio
import multiprocessing

import pytest

from core.types import AssociationType, HexagramType, MemoryLayer
from memory.system import MemorySystem


def _counts(system: MemorySystem) -> dict:
    return {
        (source, target): count
        for source, target, count, _probability in system.hexagram_model.export_state()
        if count
    }


def test_hexagram_transition_counts_survive_reopen(tmp_path):
    path = tmp_path / "shared.sqlite"
    system = MemorySystem(persist_path=str(path))
    left = asyncio.run(system.store("甲卦", HexagramType.QIAN, MemoryLayer.HUMAN))
    right = asyncio.run(system.store("乙卦", HexagramType.KUN, MemoryLayer.HUMAN))
    assert asyncio.run(system.associate(left, right, AssociationType.CAUSAL)) is True
    before_counts = _counts(system)
    before_state = system.hexagram_model.export_state()
    assert before_counts.get(("QIAN", "KUN")) == 1
    system.close()

    restored = MemorySystem(persist_path=str(path))
    try:
        assert _counts(restored) == before_counts
        after_state = restored.hexagram_model.export_state()
        assert [(row[0], row[1], row[2]) for row in after_state] == [
            (row[0], row[1], row[2]) for row in before_state
        ]
        for old, new in zip(before_state, after_state):
            assert old[3] == pytest.approx(new[3])
    finally:
        restored.close()


def _mp_store(path: str, content: str) -> None:
    system = MemorySystem(persist_path=path)
    try:
        asyncio.run(system.store(content, HexagramType.QIAN, MemoryLayer.HUMAN))
    finally:
        system.close()


def test_two_processes_write_the_same_database(tmp_path):
    path = str(tmp_path / "shared.sqlite")
    ready = MemorySystem(persist_path=path)
    ready.close()

    context = multiprocessing.get_context("fork")
    first = context.Process(target=_mp_store, args=(path, "进程甲记忆"))
    second = context.Process(target=_mp_store, args=(path, "进程乙记忆"))
    first.start()
    second.start()
    first.join(10)
    second.join(10)

    assert first.exitcode == 0
    assert second.exitcode == 0
    seen = MemorySystem(persist_path=path)
    try:
        texts = {str(memory.content) for memory in seen._memory_index.values()}
        assert texts == {"进程甲记忆", "进程乙记忆"}
    finally:
        seen.close()
