"""
Ganzhi (Heavenly Stems and Earthly Branches) Temporal-Spatial Coordinate System
干支时空坐标系统 - 为记忆系统提供时空标签和能量计算

核心组件：
- GanzhiCoordinate: 干支时空坐标数据结构
- GanzhiMarker: 干支标记器，为新记忆打上时空标签
- GanzhiQuery: 干支查询接口，支持按干支检索记忆
- GanzhiEnergyCalculator: 干支能量计算器，计算五行能量值
"""

from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import os
import importlib.util

_types_spec = importlib.util.spec_from_file_location(
    "types_module",
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "core", "types.py")
)
_types_module = importlib.util.module_from_spec(_types_spec)
_types_spec.loader.exec_module(_types_module)

TianganType = _types_module.TianganType
DizhiType = _types_module.DizhiType
WuxingType = _types_module.WuxingType
WuxingRelation = _types_module.WuxingRelation


class Tiangan(Enum):
    """天干枚举 - Ten Heavenly Stems"""
    JIA = "甲"
    YI = "乙"
    BING = "丙"
    DING = "丁"
    WU = "戊"
    JI = "己"
    GENG = "庚"
    XIN = "辛"
    REN = "壬"
    GUI = "癸"

    @classmethod
    def from_tiangan_type(cls, tiangan_type: TianganType) -> 'Tiangan':
        mapping = {
            TianganType.JIA: cls.JIA,
            TianganType.YI: cls.YI,
            TianganType.BING: cls.BING,
            TianganType.DING: cls.DING,
            TianganType.WU: cls.WU,
            TianganType.JI: cls.JI,
            TianganType.GENG: cls.GENG,
            TianganType.XIN: cls.XIN,
            TianganType.REN: cls.REN,
            TianganType.GUI: cls.GUI,
        }
        return mapping.get(tiangan_type, cls.JIA)

    def to_tiangan_type(self) -> TianganType:
        mapping = {
            self.JIA: TianganType.JIA,
            self.YI: TianganType.YI,
            self.BING: TianganType.BING,
            self.DING: TianganType.DING,
            self.WU: TianganType.WU,
            self.JI: TianganType.JI,
            self.GENG: TianganType.GENG,
            self.XIN: TianganType.XIN,
            self.REN: TianganType.REN,
            self.GUI: TianganType.GUI,
        }
        return mapping[self]


class Dizhi(Enum):
    """地支枚举 - Twelve Earthly Branches"""
    ZI = "子"
    CHOU = "丑"
    YIN = "寅"
    MAO = "卯"
    CHEN = "辰"
    SI = "巳"
    WU = "午"
    WEI = "未"
    SHEN = "申"
    YOU = "酉"
    XU = "戌"
    HAI = "亥"

    @classmethod
    def from_dizhi_type(cls, dizhi_type: DizhiType) -> 'Dizhi':
        mapping = {
            DizhiType.ZI: cls.ZI,
            DizhiType.CHOU: cls.CHOU,
            DizhiType.YIN: cls.YIN,
            DizhiType.MAO: cls.MAO,
            DizhiType.CHEN: cls.CHEN,
            DizhiType.SI: cls.SI,
            DizhiType.WU: cls.WU,
            DizhiType.WEI: cls.WEI,
            DizhiType.SHEN: cls.SHEN,
            DizhiType.YOU: cls.YOU,
            DizhiType.XU: cls.XU,
            DizhiType.HAI: cls.HAI,
        }
        return mapping.get(dizhi_type, cls.ZI)

    def to_dizhi_type(self) -> DizhiType:
        mapping = {
            self.ZI: DizhiType.ZI,
            self.CHOU: DizhiType.CHOU,
            self.YIN: DizhiType.YIN,
            self.MAO: DizhiType.MAO,
            self.CHEN: DizhiType.CHEN,
            self.SI: DizhiType.SI,
            self.WU: DizhiType.WU,
            self.WEI: DizhiType.WEI,
            self.SHEN: DizhiType.SHEN,
            self.YOU: DizhiType.YOU,
            self.XU: DizhiType.XU,
            self.HAI: DizhiType.HAI,
        }
        return mapping[self]


TIANGAN_WUXING: Dict[Tiangan, WuxingType] = {
    Tiangan.JIA: WuxingType.WOOD,
    Tiangan.YI: WuxingType.WOOD,
    Tiangan.BING: WuxingType.FIRE,
    Tiangan.DING: WuxingType.FIRE,
    Tiangan.WU: WuxingType.EARTH,
    Tiangan.JI: WuxingType.EARTH,
    Tiangan.GENG: WuxingType.METAL,
    Tiangan.XIN: WuxingType.METAL,
    Tiangan.REN: WuxingType.WATER,
    Tiangan.GUI: WuxingType.WATER,
}

DIZHI_WUXING: Dict[Dizhi, WuxingType] = {
    Dizhi.YIN: WuxingType.WOOD,
    Dizhi.MAO: WuxingType.WOOD,
    Dizhi.SI: WuxingType.FIRE,
    Dizhi.WU: WuxingType.FIRE,
    Dizhi.CHEN: WuxingType.EARTH,
    Dizhi.XU: WuxingType.EARTH,
    Dizhi.CHOU: WuxingType.EARTH,
    Dizhi.WEI: WuxingType.EARTH,
    Dizhi.SHEN: WuxingType.METAL,
    Dizhi.YOU: WuxingType.METAL,
    Dizhi.HAI: WuxingType.WATER,
    Dizhi.ZI: WuxingType.WATER,
}

TIANGAN_YINYANG: Dict[Tiangan, str] = {
    Tiangan.JIA: "阳",
    Tiangan.YI: "阴",
    Tiangan.BING: "阳",
    Tiangan.DING: "阴",
    Tiangan.WU: "阳",
    Tiangan.JI: "阴",
    Tiangan.GENG: "阳",
    Tiangan.XIN: "阴",
    Tiangan.REN: "阳",
    Tiangan.GUI: "阴",
}

DIZHI_YINYANG: Dict[Dizhi, str] = {
    Dizhi.ZI: "阳",
    Dizhi.CHOU: "阴",
    Dizhi.YIN: "阳",
    Dizhi.MAO: "阴",
    Dizhi.CHEN: "阳",
    Dizhi.SI: "阴",
    Dizhi.WU: "阳",
    Dizhi.WEI: "阴",
    Dizhi.SHEN: "阳",
    Dizhi.YOU: "阴",
    Dizhi.XU: "阳",
    Dizhi.HAI: "阴",
}


@dataclass
class SpatialPosition:
    """空间位置 - Spatial position in the Ganzhi coordinate system"""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    dimension: str = "physical"

    def to_dict(self) -> Dict[str, Any]:
        return {
            'x': self.x,
            'y': self.y,
            'z': self.z,
            'dimension': self.dimension,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SpatialPosition':
        return cls(
            x=data.get('x', 0.0),
            y=data.get('y', 0.0),
            z=data.get('z', 0.0),
            dimension=data.get('dimension', 'physical'),
        )


@dataclass
class GanzhiCoordinate:
    """
    干支时空坐标数据结构 - Ganzhi Temporal-Spatial Coordinate
    
    包含时间、空间、能量三维坐标信息
    """
    tiangan: Tiangan
    dizhi: Dizhi
    spatial_position: SpatialPosition = field(default_factory=SpatialPosition)
    energy_value: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    cycle_index: int = 0
    wuxing_energy: Dict[WuxingType, float] = field(default_factory=dict)

    def __post_init__(self):
        if not self.wuxing_energy:
            self.wuxing_energy = self._calculate_default_wuxing_energy()

    def _calculate_default_wuxing_energy(self) -> Dict[WuxingType, float]:
        calculator = GanzhiEnergyCalculator()
        return calculator.calculate_wuxing_energy(self.tiangan, self.dizhi)

    @property
    def ganzhi_name(self) -> str:
        return f"{self.tiangan.value}{self.dizhi.value}"

    @property
    def tiangan_wuxing(self) -> WuxingType:
        return TIANGAN_WUXING.get(self.tiangan, WuxingType.EARTH)

    @property
    def dizhi_wuxing(self) -> WuxingType:
        return DIZHI_WUXING.get(self.dizhi, WuxingType.EARTH)

    @property
    def tiangan_yinyang(self) -> str:
        return TIANGAN_YINYANG.get(self.tiangan, "阳")

    @property
    def dizhi_yinyang(self) -> str:
        return DIZHI_YINYANG.get(self.dizhi, "阳")

    def get_cycle_position(self) -> int:
        tiangan_idx = list(Tiangan).index(self.tiangan)
        dizhi_idx = list(Dizhi).index(self.dizhi)
        return (tiangan_idx * 6 + dizhi_idx) % 60

    def to_dict(self) -> Dict[str, Any]:
        return {
            'tiangan': self.tiangan.value,
            'dizhi': self.dizhi.value,
            'spatial_position': self.spatial_position.to_dict(),
            'energy_value': self.energy_value,
            'timestamp': self.timestamp.isoformat(),
            'cycle_index': self.cycle_index,
            'wuxing_energy': {k.value: v for k, v in self.wuxing_energy.items()},
            'ganzhi_name': self.ganzhi_name,
            'tiangan_wuxing': self.tiangan_wuxing.value,
            'dizhi_wuxing': self.dizhi_wuxing.value,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GanzhiCoordinate':
        tiangan = next((t for t in Tiangan if t.value == data['tiangan']), Tiangan.JIA)
        dizhi = next((d for d in Dizhi if d.value == data['dizhi']), Dizhi.ZI)
        
        wuxing_energy = {}
        for k, v in data.get('wuxing_energy', {}).items():
            wuxing_type = next((w for w in WuxingType if w.value == k), WuxingType.EARTH)
            wuxing_energy[wuxing_type] = v

        return cls(
            tiangan=tiangan,
            dizhi=dizhi,
            spatial_position=SpatialPosition.from_dict(data.get('spatial_position', {})),
            energy_value=data.get('energy_value', 0.0),
            timestamp=datetime.fromisoformat(data['timestamp']) if 'timestamp' in data else datetime.now(),
            cycle_index=data.get('cycle_index', 0),
            wuxing_energy=wuxing_energy,
        )


@dataclass
class MemoryRecord:
    """记忆记录 - Memory record with Ganzhi coordinate"""
    record_id: str
    content: Any
    coordinate: GanzhiCoordinate
    layer: str = "human"
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'record_id': self.record_id,
            'content': str(self.content),
            'coordinate': self.coordinate.to_dict(),
            'layer': self.layer,
            'tags': self.tags,
            'metadata': self.metadata,
        }


class GanzhiMarker:
    """
    干支标记器 - Ganzhi Marker
    
    为新记忆打上时空标签，自动计算干支
    """

    EPOCH_START = datetime(1900, 1, 1)
    EPOCH_TIANGAN_INDEX = 0
    EPOCH_DIZHI_INDEX = 0

    def __init__(self):
        self._marked_records: Dict[str, MemoryRecord] = {}

    def calculate_ganzhi(self, dt: datetime) -> Tuple[Tiangan, Dizhi]:
        """
        计算指定时间的干支
        
        Args:
            dt: 目标时间
            
        Returns:
            (天干, 地支) 元组
        """
        days_since_epoch = (dt - self.EPOCH_START).days
        tiangan_idx = (self.EPOCH_TIANGAN_INDEX + days_since_epoch) % 10
        dizhi_idx = (self.EPOCH_DIZHI_INDEX + days_since_epoch) % 12
        
        tiangan = list(Tiangan)[tiangan_idx]
        dizhi = list(Dizhi)[dizhi_idx]
        
        return tiangan, dizhi

    def calculate_hour_ganzhi(self, dt: datetime) -> Tuple[Tiangan, Dizhi]:
        """
        计算时辰干支（基于小时）
        
        时辰对应：
        子时: 23:00-01:00, 丑时: 01:00-03:00, 寅时: 03:00-05:00
        卯时: 05:00-07:00, 辰时: 07:00-09:00, 巳时: 09:00-11:00
        午时: 11:00-13:00, 未时: 13:00-15:00, 申时: 15:00-17:00
        酉时: 17:00-19:00, 戌时: 19:00-21:00, 亥时: 21:00-23:00
        """
        hour = dt.hour
        dizhi_idx = ((hour + 1) // 2) % 12
        dizhi = list(Dizhi)[dizhi_idx]
        
        day_tiangan, _ = self.calculate_ganzhi(dt)
        day_tiangan_idx = list(Tiangan).index(day_tiangan)
        tiangan_idx = (day_tiangan_idx * 5 + dizhi_idx) % 10
        tiangan = list(Tiangan)[tiangan_idx]
        
        return tiangan, dizhi

    def mark(
        self,
        content: Any,
        record_id: str,
        timestamp: Optional[datetime] = None,
        spatial_position: Optional[SpatialPosition] = None,
        layer: str = "human",
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> MemoryRecord:
        """
        为新记忆打上时空标签
        
        Args:
            content: 记忆内容
            record_id: 记录ID
            timestamp: 时间戳（默认当前时间）
            spatial_position: 空间位置
            layer: 记忆层次（heaven/earth/human）
            tags: 标签列表
            metadata: 元数据
            
        Returns:
            带有干支时空标签的记忆记录
        """
        ts = timestamp or datetime.now()
        tiangan, dizhi = self.calculate_ganzhi(ts)
        
        calculator = GanzhiEnergyCalculator()
        wuxing_energy = calculator.calculate_wuxing_energy(tiangan, dizhi)
        total_energy = sum(wuxing_energy.values())
        
        cycle_index = self._calculate_cycle_index(tiangan, dizhi)
        
        coordinate = GanzhiCoordinate(
            tiangan=tiangan,
            dizhi=dizhi,
            spatial_position=spatial_position or SpatialPosition(),
            energy_value=total_energy,
            timestamp=ts,
            cycle_index=cycle_index,
            wuxing_energy=wuxing_energy,
        )
        
        record = MemoryRecord(
            record_id=record_id,
            content=content,
            coordinate=coordinate,
            layer=layer,
            tags=tags or [],
            metadata=metadata or {},
        )
        
        self._marked_records[record_id] = record
        return record

    def _calculate_cycle_index(self, tiangan: Tiangan, dizhi: Dizhi) -> int:
        """计算在60甲子循环中的位置（0-59）"""
        tiangan_idx = list(Tiangan).index(tiangan)
        dizhi_idx = list(Dizhi).index(dizhi)
        
        for i in range(60):
            if (i % 10) == tiangan_idx and (i % 12) == dizhi_idx:
                return i
        return 0

    def get_marked_record(self, record_id: str) -> Optional[MemoryRecord]:
        """获取已标记的记录"""
        return self._marked_records.get(record_id)

    def get_all_marked_records(self) -> List[MemoryRecord]:
        """获取所有已标记的记录"""
        return list(self._marked_records.values())


class GanzhiQuery:
    """
    干支查询接口 - Ganzhi Query Interface
    
    支持按干支、周期、五行等条件检索记忆
    """

    def __init__(self, marker: Optional[GanzhiMarker] = None):
        self.marker = marker or GanzhiMarker()

    def query_by_ganzhi(
        self,
        records: List[MemoryRecord],
        tiangan: Optional[Tiangan] = None,
        dizhi: Optional[Dizhi] = None,
        exact_match: bool = True,
    ) -> List[MemoryRecord]:
        """
        按干支检索记忆
        
        Args:
            records: 记忆记录列表
            tiangan: 天干（可选）
            dizhi: 地支（可选）
            exact_match: 是否精确匹配（天干和地支都匹配）
            
        Returns:
            匹配的记忆记录列表
        """
        results = []
        
        for record in records:
            coord = record.coordinate
            
            if exact_match:
                if tiangan and dizhi:
                    if coord.tiangan == tiangan and coord.dizhi == dizhi:
                        results.append(record)
                elif tiangan:
                    if coord.tiangan == tiangan:
                        results.append(record)
                elif dizhi:
                    if coord.dizhi == dizhi:
                        results.append(record)
            else:
                match = True
                if tiangan and coord.tiangan != tiangan:
                    match = False
                if dizhi and coord.dizhi != dizhi:
                    match = False
                if match:
                    results.append(record)
        
        return results

    def query_by_cycle(
        self,
        records: List[MemoryRecord],
        cycle_start: int,
        cycle_end: int,
    ) -> List[MemoryRecord]:
        """
        按周期检索记忆
        
        Args:
            records: 记忆记录列表
            cycle_start: 周期起始位置（0-59）
            cycle_end: 周期结束位置（0-59）
            
        Returns:
            匹配的记忆记录列表
        """
        results = []
        
        for record in records:
            cycle_idx = record.coordinate.cycle_index
            
            if cycle_start <= cycle_end:
                if cycle_start <= cycle_idx <= cycle_end:
                    results.append(record)
            else:
                if cycle_idx >= cycle_start or cycle_idx <= cycle_end:
                    results.append(record)
        
        return results

    def query_by_wuxing(
        self,
        records: List[MemoryRecord],
        wuxing: WuxingType,
        include_tiangan: bool = True,
        include_dizhi: bool = True,
    ) -> List[MemoryRecord]:
        """
        按五行检索记忆
        
        Args:
            records: 记忆记录列表
            wuxing: 五行类型
            include_tiangan: 是否匹配天干五行
            include_dizhi: 是否匹配地支五行
            
        Returns:
            匹配的记忆记录列表
        """
        results = []
        
        for record in records:
            coord = record.coordinate
            match = False
            
            if include_tiangan and coord.tiangan_wuxing == wuxing:
                match = True
            if include_dizhi and coord.dizhi_wuxing == wuxing:
                match = True
            
            if match:
                results.append(record)
        
        return results

    def query_by_yinyang(
        self,
        records: List[MemoryRecord],
        yinyang: str,
        include_tiangan: bool = True,
        include_dizhi: bool = True,
    ) -> List[MemoryRecord]:
        """
        按阴阳检索记忆
        
        Args:
            records: 记忆记录列表
            yinyang: 阴阳属性（"阴"或"阳"）
            include_tiangan: 是否匹配天干阴阳
            include_dizhi: 是否匹配地支阴阳
            
        Returns:
            匹配的记忆记录列表
        """
        results = []
        
        for record in records:
            coord = record.coordinate
            match = False
            
            if include_tiangan and coord.tiangan_yinyang == yinyang:
                match = True
            if include_dizhi and coord.dizhi_yinyang == yinyang:
                match = True
            
            if match:
                results.append(record)
        
        return results

    def query_by_time_range(
        self,
        records: List[MemoryRecord],
        start_time: datetime,
        end_time: datetime,
    ) -> List[MemoryRecord]:
        """
        按时间范围检索记忆
        
        Args:
            records: 记忆记录列表
            start_time: 起始时间
            end_time: 结束时间
            
        Returns:
            匹配的记忆记录列表
        """
        results = []
        
        for record in records:
            ts = record.coordinate.timestamp
            if start_time <= ts <= end_time:
                results.append(record)
        
        return results

    def query_by_energy_range(
        self,
        records: List[MemoryRecord],
        min_energy: float,
        max_energy: float,
    ) -> List[MemoryRecord]:
        """
        按能量范围检索记忆
        
        Args:
            records: 记忆记录列表
            min_energy: 最小能量值
            max_energy: 最大能量值
            
        Returns:
            匹配的记忆记录列表
        """
        results = []
        
        for record in records:
            energy = record.coordinate.energy_value
            if min_energy <= energy <= max_energy:
                results.append(record)
        
        return results

    def get_ganzhi_statistics(
        self,
        records: List[MemoryRecord],
    ) -> Dict[str, Any]:
        """
        获取干支统计信息
        
        Args:
            records: 记忆记录列表
            
        Returns:
            统计信息字典
        """
        tiangan_count: Dict[Tiangan, int] = {t: 0 for t in Tiangan}
        dizhi_count: Dict[Dizhi, int] = {d: 0 for d in Dizhi}
        wuxing_count: Dict[WuxingType, int] = {w: 0 for w in WuxingType}
        
        for record in records:
            coord = record.coordinate
            tiangan_count[coord.tiangan] += 1
            dizhi_count[coord.dizhi] += 1
            wuxing_count[coord.tiangan_wuxing] += 1
            wuxing_count[coord.dizhi_wuxing] += 1
        
        return {
            'total_records': len(records),
            'tiangan_distribution': {t.value: c for t, c in tiangan_count.items()},
            'dizhi_distribution': {d.value: c for d, c in dizhi_count.items()},
            'wuxing_distribution': {w.value: c for w, c in wuxing_count.items()},
        }


class GanzhiEnergyCalculator:
    """
    干支能量计算器 - Ganzhi Energy Calculator
    
    根据干支属性计算五行能量值
    """

    WUXING_GENERATION = {
        WuxingType.WOOD: WuxingType.FIRE,
        WuxingType.FIRE: WuxingType.EARTH,
        WuxingType.EARTH: WuxingType.METAL,
        WuxingType.METAL: WuxingType.WATER,
        WuxingType.WATER: WuxingType.WOOD,
    }

    WUXING_RESTRICTION = {
        WuxingType.WOOD: WuxingType.EARTH,
        WuxingType.EARTH: WuxingType.WATER,
        WuxingType.WATER: WuxingType.FIRE,
        WuxingType.FIRE: WuxingType.METAL,
        WuxingType.METAL: WuxingType.WOOD,
    }

    BASE_ENERGY: Dict[WuxingType, float] = {
        WuxingType.WOOD: 1.0,
        WuxingType.FIRE: 1.0,
        WuxingType.EARTH: 1.0,
        WuxingType.METAL: 1.0,
        WuxingType.WATER: 1.0,
    }

    def calculate_wuxing_energy(
        self,
        tiangan: Tiangan,
        dizhi: Dizhi,
    ) -> Dict[WuxingType, float]:
        """
        计算五行能量值
        
        基于天干和地支的五行属性，计算各五行能量值：
        - 天干五行贡献基础能量
        - 地支五行贡献基础能量
        - 天干地支五行相生则增强
        - 天干地支五行相克则减弱
        
        Args:
            tiangan: 天干
            dizhi: 地支
            
        Returns:
            各五行能量值字典
        """
        energy = dict(self.BASE_ENERGY)
        
        gan_wuxing = TIANGAN_WUXING.get(tiangan, WuxingType.EARTH)
        zhi_wuxing = DIZHI_WUXING.get(dizhi, WuxingType.EARTH)
        
        energy[gan_wuxing] += 0.5
        energy[zhi_wuxing] += 0.5
        
        if gan_wuxing == zhi_wuxing:
            energy[gan_wuxing] += 0.3
        
        if self.WUXING_GENERATION.get(gan_wuxing) == zhi_wuxing:
            energy[zhi_wuxing] += 0.3
        elif self.WUXING_GENERATION.get(zhi_wuxing) == gan_wuxing:
            energy[gan_wuxing] += 0.3
        
        if self.WUXING_RESTRICTION.get(gan_wuxing) == zhi_wuxing:
            energy[zhi_wuxing] -= 0.2
        elif self.WUXING_RESTRICTION.get(zhi_wuxing) == gan_wuxing:
            energy[gan_wuxing] -= 0.2
        
        for wuxing in WuxingType:
            energy[wuxing] = max(0.1, min(2.0, energy[wuxing]))
        
        return energy

    def calculate_total_energy(
        self,
        tiangan: Tiangan,
        dizhi: Dizhi,
    ) -> float:
        """
        计算总能量值
        
        Args:
            tiangan: 天干
            dizhi: 地支
            
        Returns:
            总能量值
        """
        wuxing_energy = self.calculate_wuxing_energy(tiangan, dizhi)
        return sum(wuxing_energy.values())

    def calculate_energy_balance(
        self,
        tiangan: Tiangan,
        dizhi: Dizhi,
    ) -> float:
        """
        计算能量平衡度
        
        Args:
            tiangan: 天干
            dizhi: 地支
            
        Returns:
            平衡度（0.0-1.0，1.0表示完全平衡）
        """
        wuxing_energy = self.calculate_wuxing_energy(tiangan, dizhi)
        values = list(wuxing_energy.values())
        
        avg = sum(values) / len(values)
        variance = sum((v - avg) ** 2 for v in values) / len(values)
        max_variance = 0.5
        
        balance = 1.0 - min(1.0, variance / max_variance)
        return balance

    def get_dominant_wuxing(
        self,
        tiangan: Tiangan,
        dizhi: Dizhi,
    ) -> WuxingType:
        """
        获取主导五行
        
        Args:
            tiangan: 天干
            dizhi: 地支
            
        Returns:
            能量最强的五行类型
        """
        wuxing_energy = self.calculate_wuxing_energy(tiangan, dizhi)
        return max(wuxing_energy.items(), key=lambda x: x[1])[0]

    def get_wuxing_relation(
        self,
        tiangan: Tiangan,
        dizhi: Dizhi,
    ) -> WuxingRelation:
        """
        获取天干地支五行关系
        
        Args:
            tiangan: 天干
            dizhi: 地支
            
        Returns:
            五行关系类型
        """
        gan_wuxing = TIANGAN_WUXING.get(tiangan, WuxingType.EARTH)
        zhi_wuxing = DIZHI_WUXING.get(dizhi, WuxingType.EARTH)
        
        if gan_wuxing == zhi_wuxing:
            return WuxingRelation.SAME_NATURE
        elif self.WUXING_GENERATION.get(gan_wuxing) == zhi_wuxing:
            return WuxingRelation.GENERATE
        elif self.WUXING_GENERATION.get(zhi_wuxing) == gan_wuxing:
            return WuxingRelation.GENERATE
        elif self.WUXING_RESTRICTION.get(gan_wuxing) == zhi_wuxing:
            return WuxingRelation.RESTRICT
        elif self.WUXING_RESTRICTION.get(zhi_wuxing) == gan_wuxing:
            return WuxingRelation.RESTRICT
        else:
            return WuxingRelation.SAME_NATURE

    def calculate_compatibility(
        self,
        coord1: GanzhiCoordinate,
        coord2: GanzhiCoordinate,
    ) -> float:
        """
        计算两个干支坐标的兼容性
        
        Args:
            coord1: 第一个干支坐标
            coord2: 第二个干支坐标
            
        Returns:
            兼容性分数（0.0-1.0）
        """
        wuxing_energy1 = coord1.wuxing_energy
        wuxing_energy2 = coord2.wuxing_energy
        
        compatibility = 0.0
        
        for wuxing in WuxingType:
            e1 = wuxing_energy1.get(wuxing, 1.0)
            e2 = wuxing_energy2.get(wuxing, 1.0)
            
            diff = abs(e1 - e2)
            similarity = 1.0 - min(1.0, diff / 1.0)
            compatibility += similarity
        
        compatibility /= len(WuxingType)
        
        gan1_wuxing = TIANGAN_WUXING.get(coord1.tiangan, WuxingType.EARTH)
        gan2_wuxing = TIANGAN_WUXING.get(coord2.tiangan, WuxingType.EARTH)
        
        if self.WUXING_GENERATION.get(gan1_wuxing) == gan2_wuxing:
            compatibility += 0.1
        elif self.WUXING_GENERATION.get(gan2_wuxing) == gan1_wuxing:
            compatibility += 0.1
        
        return min(1.0, compatibility)

    def get_energy_analysis(
        self,
        tiangan: Tiangan,
        dizhi: Dizhi,
    ) -> Dict[str, Any]:
        """
        获取完整的能量分析
        
        Args:
            tiangan: 天干
            dizhi: 地支
            
        Returns:
            能量分析结果字典
        """
        wuxing_energy = self.calculate_wuxing_energy(tiangan, dizhi)
        total_energy = self.calculate_total_energy(tiangan, dizhi)
        balance = self.calculate_energy_balance(tiangan, dizhi)
        dominant = self.get_dominant_wuxing(tiangan, dizhi)
        relation = self.get_wuxing_relation(tiangan, dizhi)
        
        return {
            'tiangan': tiangan.value,
            'dizhi': dizhi.value,
            'tiangan_wuxing': TIANGAN_WUXING.get(tiangan, WuxingType.EARTH).value,
            'dizhi_wuxing': DIZHI_WUXING.get(dizhi, WuxingType.EARTH).value,
            'tiangan_yinyang': TIANGAN_YINYANG.get(tiangan, "阳"),
            'dizhi_yinyang': DIZHI_YINYANG.get(dizhi, "阳"),
            'wuxing_energy': {k.value: v for k, v in wuxing_energy.items()},
            'total_energy': total_energy,
            'energy_balance': balance,
            'dominant_wuxing': dominant.value,
            'wuxing_relation': relation.value,
        }
