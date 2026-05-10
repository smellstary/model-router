"""
Standalone test script for Ganzhi Temporal-Spatial Coordinate System
干支时空坐标系统独立测试脚本
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import importlib.util

ganzhi_spec = importlib.util.spec_from_file_location(
    "ganzhi_coordinate",
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "memory", "ganzhi_coordinate.py")
)
ganzhi_module = importlib.util.module_from_spec(ganzhi_spec)
ganzhi_spec.loader.exec_module(ganzhi_module)

Tiangan = ganzhi_module.Tiangan
Dizhi = ganzhi_module.Dizhi
TIANGAN_WUXING = ganzhi_module.TIANGAN_WUXING
DIZHI_WUXING = ganzhi_module.DIZHI_WUXING
TIANGAN_YINYANG = ganzhi_module.TIANGAN_YINYANG
DIZHI_YINYANG = ganzhi_module.DIZHI_YINYANG
SpatialPosition = ganzhi_module.SpatialPosition
GanzhiCoordinate = ganzhi_module.GanzhiCoordinate
MemoryRecord = ganzhi_module.MemoryRecord
GanzhiMarker = ganzhi_module.GanzhiMarker
GanzhiQuery = ganzhi_module.GanzhiQuery
GanzhiEnergyCalculator = ganzhi_module.GanzhiEnergyCalculator
WuxingType = ganzhi_module.WuxingType
WuxingRelation = ganzhi_module.WuxingRelation

from datetime import datetime

def test_tiangan_enum():
    print("测试天干枚举...")
    assert Tiangan.JIA.value == "甲"
    assert Tiangan.YI.value == "乙"
    assert Tiangan.BING.value == "丙"
    assert Tiangan.DING.value == "丁"
    assert Tiangan.WU.value == "戊"
    assert Tiangan.JI.value == "己"
    assert Tiangan.GENG.value == "庚"
    assert Tiangan.XIN.value == "辛"
    assert Tiangan.REN.value == "壬"
    assert Tiangan.GUI.value == "癸"
    assert len(Tiangan) == 10
    print("  ✓ 天干枚举测试通过")

def test_dizhi_enum():
    print("测试地支枚举...")
    assert Dizhi.ZI.value == "子"
    assert Dizhi.CHOU.value == "丑"
    assert Dizhi.YIN.value == "寅"
    assert Dizhi.MAO.value == "卯"
    assert Dizhi.CHEN.value == "辰"
    assert Dizhi.SI.value == "巳"
    assert Dizhi.WU.value == "午"
    assert Dizhi.WEI.value == "未"
    assert Dizhi.SHEN.value == "申"
    assert Dizhi.YOU.value == "酉"
    assert Dizhi.XU.value == "戌"
    assert Dizhi.HAI.value == "亥"
    assert len(Dizhi) == 12
    print("  ✓ 地支枚举测试通过")

def test_tiangan_wuxing():
    print("测试天干五行属性...")
    assert TIANGAN_WUXING[Tiangan.JIA] == WuxingType.WOOD
    assert TIANGAN_WUXING[Tiangan.YI] == WuxingType.WOOD
    assert TIANGAN_WUXING[Tiangan.BING] == WuxingType.FIRE
    assert TIANGAN_WUXING[Tiangan.DING] == WuxingType.FIRE
    assert TIANGAN_WUXING[Tiangan.WU] == WuxingType.EARTH
    assert TIANGAN_WUXING[Tiangan.JI] == WuxingType.EARTH
    assert TIANGAN_WUXING[Tiangan.GENG] == WuxingType.METAL
    assert TIANGAN_WUXING[Tiangan.XIN] == WuxingType.METAL
    assert TIANGAN_WUXING[Tiangan.REN] == WuxingType.WATER
    assert TIANGAN_WUXING[Tiangan.GUI] == WuxingType.WATER
    print("  ✓ 天干五行属性测试通过")

def test_dizhi_wuxing():
    print("测试地支五行属性...")
    assert DIZHI_WUXING[Dizhi.YIN] == WuxingType.WOOD
    assert DIZHI_WUXING[Dizhi.MAO] == WuxingType.WOOD
    assert DIZHI_WUXING[Dizhi.SI] == WuxingType.FIRE
    assert DIZHI_WUXING[Dizhi.WU] == WuxingType.FIRE
    assert DIZHI_WUXING[Dizhi.CHEN] == WuxingType.EARTH
    assert DIZHI_WUXING[Dizhi.XU] == WuxingType.EARTH
    assert DIZHI_WUXING[Dizhi.CHOU] == WuxingType.EARTH
    assert DIZHI_WUXING[Dizhi.WEI] == WuxingType.EARTH
    assert DIZHI_WUXING[Dizhi.SHEN] == WuxingType.METAL
    assert DIZHI_WUXING[Dizhi.YOU] == WuxingType.METAL
    assert DIZHI_WUXING[Dizhi.HAI] == WuxingType.WATER
    assert DIZHI_WUXING[Dizhi.ZI] == WuxingType.WATER
    print("  ✓ 地支五行属性测试通过")

def test_tiangan_yinyang():
    print("测试天干阴阳属性...")
    assert TIANGAN_YINYANG[Tiangan.JIA] == "阳"
    assert TIANGAN_YINYANG[Tiangan.BING] == "阳"
    assert TIANGAN_YINYANG[Tiangan.WU] == "阳"
    assert TIANGAN_YINYANG[Tiangan.GENG] == "阳"
    assert TIANGAN_YINYANG[Tiangan.REN] == "阳"
    assert TIANGAN_YINYANG[Tiangan.YI] == "阴"
    assert TIANGAN_YINYANG[Tiangan.DING] == "阴"
    assert TIANGAN_YINYANG[Tiangan.JI] == "阴"
    assert TIANGAN_YINYANG[Tiangan.XIN] == "阴"
    assert TIANGAN_YINYANG[Tiangan.GUI] == "阴"
    print("  ✓ 天干阴阳属性测试通过")

def test_dizhi_yinyang():
    print("测试地支阴阳属性...")
    assert DIZHI_YINYANG[Dizhi.ZI] == "阳"
    assert DIZHI_YINYANG[Dizhi.YIN] == "阳"
    assert DIZHI_YINYANG[Dizhi.CHEN] == "阳"
    assert DIZHI_YINYANG[Dizhi.WU] == "阳"
    assert DIZHI_YINYANG[Dizhi.SHEN] == "阳"
    assert DIZHI_YINYANG[Dizhi.XU] == "阳"
    assert DIZHI_YINYANG[Dizhi.CHOU] == "阴"
    assert DIZHI_YINYANG[Dizhi.MAO] == "阴"
    assert DIZHI_YINYANG[Dizhi.SI] == "阴"
    assert DIZHI_YINYANG[Dizhi.WEI] == "阴"
    assert DIZHI_YINYANG[Dizhi.YOU] == "阴"
    assert DIZHI_YINYANG[Dizhi.HAI] == "阴"
    print("  ✓ 地支阴阳属性测试通过")

def test_spatial_position():
    print("测试空间位置...")
    pos = SpatialPosition()
    assert pos.x == 0.0
    assert pos.y == 0.0
    assert pos.z == 0.0
    assert pos.dimension == "physical"
    
    pos = SpatialPosition(x=1.0, y=2.0, z=3.0, dimension="spiritual")
    assert pos.x == 1.0
    assert pos.y == 2.0
    assert pos.z == 3.0
    assert pos.dimension == "spiritual"
    
    data = pos.to_dict()
    assert data['x'] == 1.0
    assert data['y'] == 2.0
    
    pos2 = SpatialPosition.from_dict(data)
    assert pos2.x == 1.0
    print("  ✓ 空间位置测试通过")

def test_ganzhi_coordinate():
    print("测试干支时空坐标...")
    coord = GanzhiCoordinate(tiangan=Tiangan.JIA, dizhi=Dizhi.ZI)
    assert coord.tiangan == Tiangan.JIA
    assert coord.dizhi == Dizhi.ZI
    assert coord.ganzhi_name == "甲子"
    assert coord.tiangan_wuxing == WuxingType.WOOD
    assert coord.dizhi_wuxing == WuxingType.WATER
    assert coord.tiangan_yinyang == "阳"
    assert coord.dizhi_yinyang == "阳"
    
    data = coord.to_dict()
    assert data['tiangan'] == "甲"
    assert data['dizhi'] == "子"
    assert data['ganzhi_name'] == "甲子"
    print("  ✓ 干支时空坐标测试通过")

def test_ganzhi_marker():
    print("测试干支标记器...")
    marker = GanzhiMarker()
    
    dt = datetime(2024, 1, 1)
    tiangan, dizhi = marker.calculate_ganzhi(dt)
    assert isinstance(tiangan, Tiangan)
    assert isinstance(dizhi, Dizhi)
    
    record = marker.mark(content="测试记忆内容", record_id="test_001")
    assert record.record_id == "test_001"
    assert record.content == "测试记忆内容"
    assert record.coordinate.tiangan is not None
    assert record.coordinate.dizhi is not None
    
    retrieved = marker.get_marked_record("test_001")
    assert retrieved is not None
    assert retrieved.record_id == "test_001"
    
    all_records = marker.get_all_marked_records()
    assert len(all_records) >= 1
    print("  ✓ 干支标记器测试通过")

def test_ganzhi_query():
    print("测试干支查询接口...")
    marker = GanzhiMarker()
    query = GanzhiQuery(marker)
    
    records = []
    records.append(marker.mark(content="甲子记忆", record_id="jiazi_001", timestamp=datetime(2024, 1, 1)))
    records.append(marker.mark(content="乙丑记忆", record_id="yichou_001", timestamp=datetime(2024, 1, 2)))
    records.append(marker.mark(content="丙寅记忆", record_id="bingyin_001", timestamp=datetime(2024, 1, 3)))
    
    results = query.query_by_ganzhi(records, tiangan=Tiangan.JIA)
    assert isinstance(results, list)
    
    results = query.query_by_cycle(records, cycle_start=0, cycle_end=10)
    assert isinstance(results, list)
    
    results = query.query_by_wuxing(records, wuxing=WuxingType.WOOD)
    assert isinstance(results, list)
    
    stats = query.get_ganzhi_statistics(records)
    assert 'total_records' in stats
    assert 'tiangan_distribution' in stats
    print("  ✓ 干支查询接口测试通过")

def test_ganzhi_energy_calculator():
    print("测试干支能量计算器...")
    calculator = GanzhiEnergyCalculator()
    
    energy = calculator.calculate_wuxing_energy(Tiangan.JIA, Dizhi.ZI)
    assert WuxingType.WOOD in energy
    assert WuxingType.FIRE in energy
    assert WuxingType.EARTH in energy
    assert WuxingType.METAL in energy
    assert WuxingType.WATER in energy
    
    for wuxing, value in energy.items():
        assert 0.1 <= value <= 2.0
    
    total = calculator.calculate_total_energy(Tiangan.JIA, Dizhi.ZI)
    assert total > 0
    
    balance = calculator.calculate_energy_balance(Tiangan.JIA, Dizhi.ZI)
    assert 0.0 <= balance <= 1.0
    
    dominant = calculator.get_dominant_wuxing(Tiangan.JIA, Dizhi.ZI)
    assert dominant in WuxingType
    
    relation = calculator.get_wuxing_relation(Tiangan.JIA, Dizhi.YIN)
    assert relation == WuxingRelation.SAME_NATURE
    
    analysis = calculator.get_energy_analysis(Tiangan.JIA, Dizhi.ZI)
    assert 'tiangan' in analysis
    assert 'dizhi' in analysis
    assert 'wuxing_energy' in analysis
    print("  ✓ 干支能量计算器测试通过")

def test_integration():
    print("测试集成功能...")
    marker = GanzhiMarker()
    query = GanzhiQuery(marker)
    calculator = GanzhiEnergyCalculator()
    
    record1 = marker.mark(content="第一条记忆", record_id="integration_001", layer="human", tags=["重要", "测试"])
    record2 = marker.mark(content="第二条记忆", record_id="integration_002", layer="earth", tags=["普通"])
    
    all_records = marker.get_all_marked_records()
    assert len(all_records) >= 2
    
    energy1 = calculator.calculate_wuxing_energy(record1.coordinate.tiangan, record1.coordinate.dizhi)
    assert len(energy1) == 5
    
    stats = query.get_ganzhi_statistics(all_records)
    assert stats['total_records'] >= 2
    print("  ✓ 集成功能测试通过")

def main():
    print("=" * 60)
    print("干支时空坐标系统测试")
    print("=" * 60)
    
    tests = [
        test_tiangan_enum,
        test_dizhi_enum,
        test_tiangan_wuxing,
        test_dizhi_wuxing,
        test_tiangan_yinyang,
        test_dizhi_yinyang,
        test_spatial_position,
        test_ganzhi_coordinate,
        test_ganzhi_marker,
        test_ganzhi_query,
        test_ganzhi_energy_calculator,
        test_integration,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  ✗ 测试失败: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
