"""
Meridian Energy Network System
经络能量网络系统

Implements the Twelve Regular Meridians (十二正经) and Eight Extraordinary Meridians (奇经八脉)
as an energy flow network with blockage detection and clearing mechanisms.

十二正经: 手三阴、手三阳、足三阴、足三阳
奇经八脉: 任脉、督脉、冲脉、带脉、阴阳跷脉、阴阳维脉
"""

from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime
import math


class MeridianType(Enum):
    """经络类型枚举 - Meridian Type Enumeration"""
    HAND_TAIYIN_LUNG = "手太阴肺经"
    HAND_JUEYIN_PERICARDIUM = "手厥阴心包经"
    HAND_SHAOYIN_HEART = "手少阴心经"
    HAND_YANGMING_LARGE_INTESTINE = "手阳明大肠经"
    HAND_SHAOYANG_TRIPLE_BURNER = "手少阳三焦经"
    HAND_TAIYANG_SMALL_INTESTINE = "手太阳小肠经"
    FOOT_TAIYIN_SPLEEN = "足太阴脾经"
    FOOT_JUEYIN_LIVER = "足厥阴肝经"
    FOOT_SHAOYIN_KIDNEY = "足少阴肾经"
    FOOT_YANGMING_STOMACH = "足阳明胃经"
    FOOT_SHAOYANG_GALLBLADDER = "足少阳胆经"
    FOOT_TAIYANG_BLADDER = "足太阳膀胱经"
    REN_MAI = "任脉"
    DU_MAI = "督脉"
    CHONG_MAI = "冲脉"
    DAI_MAI = "带脉"
    YIN_QIAO_MAI = "阴跷脉"
    YANG_QIAO_MAI = "阳跷脉"
    YIN_WEI_MAI = "阴维脉"
    YANG_WEI_MAI = "阳维脉"

    @classmethod
    def get_twelve_regular(cls) -> List['MeridianType']:
        """获取十二正经"""
        return [
            cls.HAND_TAIYIN_LUNG,
            cls.HAND_JUEYIN_PERICARDIUM,
            cls.HAND_SHAOYIN_HEART,
            cls.HAND_YANGMING_LARGE_INTESTINE,
            cls.HAND_SHAOYANG_TRIPLE_BURNER,
            cls.HAND_TAIYANG_SMALL_INTESTINE,
            cls.FOOT_TAIYIN_SPLEEN,
            cls.FOOT_JUEYIN_LIVER,
            cls.FOOT_SHAOYIN_KIDNEY,
            cls.FOOT_YANGMING_STOMACH,
            cls.FOOT_SHAOYANG_GALLBLADDER,
            cls.FOOT_TAIYANG_BLADDER,
        ]

    @classmethod
    def get_eight_extraordinary(cls) -> List['MeridianType']:
        """获取奇经八脉"""
        return [
            cls.REN_MAI,
            cls.DU_MAI,
            cls.CHONG_MAI,
            cls.DAI_MAI,
            cls.YIN_QIAO_MAI,
            cls.YANG_QIAO_MAI,
            cls.YIN_WEI_MAI,
            cls.YANG_WEI_MAI,
        ]

    @classmethod
    def get_hand_three_yin(cls) -> List['MeridianType']:
        """获取手三阴"""
        return [
            cls.HAND_TAIYIN_LUNG,
            cls.HAND_JUEYIN_PERICARDIUM,
            cls.HAND_SHAOYIN_HEART,
        ]

    @classmethod
    def get_hand_three_yang(cls) -> List['MeridianType']:
        """获取手三阳"""
        return [
            cls.HAND_YANGMING_LARGE_INTESTINE,
            cls.HAND_SHAOYANG_TRIPLE_BURNER,
            cls.HAND_TAIYANG_SMALL_INTESTINE,
        ]

    @classmethod
    def get_foot_three_yin(cls) -> List['MeridianType']:
        """获取足三阴"""
        return [
            cls.FOOT_TAIYIN_SPLEEN,
            cls.FOOT_JUEYIN_LIVER,
            cls.FOOT_SHAOYIN_KIDNEY,
        ]

    @classmethod
    def get_foot_three_yang(cls) -> List['MeridianType']:
        """获取足三阳"""
        return [
            cls.FOOT_YANGMING_STOMACH,
            cls.FOOT_SHAOYANG_GALLBLADDER,
            cls.FOOT_TAIYANG_BLADDER,
        ]

    def is_yin(self) -> bool:
        """判断是否为阴经"""
        return self in [
            MeridianType.HAND_TAIYIN_LUNG,
            MeridianType.HAND_JUEYIN_PERICARDIUM,
            MeridianType.HAND_SHAOYIN_HEART,
            MeridianType.FOOT_TAIYIN_SPLEEN,
            MeridianType.FOOT_JUEYIN_LIVER,
            MeridianType.FOOT_SHAOYIN_KIDNEY,
            MeridianType.REN_MAI,
            MeridianType.YIN_QIAO_MAI,
            MeridianType.YIN_WEI_MAI,
        ]

    def is_yang(self) -> bool:
        """判断是否为阳经"""
        return not self.is_yin()

    def is_regular(self) -> bool:
        """判断是否为正经"""
        return self in self.get_twelve_regular()

    def is_extraordinary(self) -> bool:
        """判断是否为奇经"""
        return self in self.get_eight_extraordinary()


class MeridianCategory(Enum):
    """经络分类"""
    HAND_THREE_YIN = "手三阴"
    HAND_THREE_YANG = "手三阳"
    FOOT_THREE_YIN = "足三阴"
    FOOT_THREE_YANG = "足三阳"
    EXTRAORDINARY = "奇经八脉"


@dataclass
class MeridianChannel:
    """经络通道数据结构 - Meridian Channel Data Structure"""
    channel_id: str
    name: str
    meridian_type: MeridianType
    connected_modules: List[str] = field(default_factory=list)
    connected_organs: List[str] = field(default_factory=list)
    flow_rate: float = 1.0
    blockage_level: float = 0.0
    energy_level: float = 1.0
    max_capacity: float = 100.0
    current_energy: float = 50.0
    connected_channels: List[str] = field(default_factory=list)
    acupoints: List[str] = field(default_factory=list)
    active_hours: Tuple[int, int] = (0, 24)
    last_flow_time: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not 0.0 <= self.flow_rate <= 2.0:
            raise ValueError(f"flow_rate must be between 0 and 2, got {self.flow_rate}")
        if not 0.0 <= self.blockage_level <= 1.0:
            raise ValueError(f"blockage_level must be between 0 and 1, got {self.blockage_level}")

    @property
    def patency(self) -> float:
        """通畅度 - 计算基于堵塞程度的通畅度"""
        return 1.0 - self.blockage_level

    @property
    def effective_flow_rate(self) -> float:
        """有效流动速率 - 受通畅度影响"""
        return self.flow_rate * self.patency

    def update_flow_rate(self, delta: float) -> float:
        """更新流动速率"""
        self.flow_rate = max(0.0, min(2.0, self.flow_rate + delta))
        return self.flow_rate

    def update_blockage(self, delta: float) -> float:
        """更新堵塞程度"""
        self.blockage_level = max(0.0, min(1.0, self.blockage_level + delta))
        return self.blockage_level

    def add_connected_module(self, module_id: str) -> None:
        """添加连接的功能模块"""
        if module_id not in self.connected_modules:
            self.connected_modules.append(module_id)

    def remove_connected_module(self, module_id: str) -> bool:
        """移除连接的功能模块"""
        if module_id in self.connected_modules:
            self.connected_modules.remove(module_id)
            return True
        return False

    def add_connected_channel(self, channel_id: str) -> None:
        """添加连接的经络通道"""
        if channel_id not in self.connected_channels:
            self.connected_channels.append(channel_id)

    def receive_energy(self, amount: float) -> float:
        """接收能量"""
        available_capacity = self.max_capacity - self.current_energy
        received = min(amount, available_capacity)
        self.current_energy += received
        return received

    def transmit_energy(self, amount: float) -> float:
        """传输能量"""
        transmitted = min(amount, self.current_energy)
        self.current_energy -= transmitted
        return transmitted

    def is_blocked(self) -> bool:
        """判断是否堵塞"""
        return self.blockage_level > 0.5

    def is_optimal(self) -> bool:
        """判断是否处于最佳状态"""
        return self.blockage_level < 0.1 and 0.8 <= self.flow_rate <= 1.2

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "channel_id": self.channel_id,
            "name": self.name,
            "meridian_type": self.meridian_type.value,
            "connected_modules": self.connected_modules,
            "connected_organs": self.connected_organs,
            "flow_rate": self.flow_rate,
            "blockage_level": self.blockage_level,
            "energy_level": self.energy_level,
            "patency": self.patency,
            "effective_flow_rate": self.effective_flow_rate,
            "current_energy": self.current_energy,
            "max_capacity": self.max_capacity,
            "is_blocked": self.is_blocked(),
        }


@dataclass
class EnergyFlowResult:
    """能量流动结果"""
    source_channel: str
    target_channel: str
    energy_amount: float
    actual_transferred: float
    flow_rate: float
    blockage_encountered: bool
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class BlockageInfo:
    """堵塞信息"""
    channel_id: str
    channel_name: str
    blockage_level: float
    location: str
    severity: str
    suggested_actions: List[str] = field(default_factory=list)
    affected_modules: List[str] = field(default_factory=list)


class MeridianNetwork:
    """经络能量网络主类 - Meridian Energy Network Main Class"""

    FLOW_DECAY_FACTOR = 0.05
    BLOCKAGE_THRESHOLD_LOW = 0.3
    BLOCKAGE_THRESHOLD_MEDIUM = 0.6
    BLOCKAGE_THRESHOLD_HIGH = 0.8
    CLEARING_BASE_RATE = 0.1
    ENERGY_ROUTING_PENALTY = 0.1

    TWELVE_REGULAR_FLOW_ORDER = [
        MeridianType.HAND_TAIYIN_LUNG,
        MeridianType.HAND_YANGMING_LARGE_INTESTINE,
        MeridianType.FOOT_YANGMING_STOMACH,
        MeridianType.FOOT_TAIYIN_SPLEEN,
        MeridianType.HAND_SHAOYIN_HEART,
        MeridianType.HAND_TAIYANG_SMALL_INTESTINE,
        MeridianType.FOOT_TAIYANG_BLADDER,
        MeridianType.FOOT_SHAOYIN_KIDNEY,
        MeridianType.HAND_JUEYIN_PERICARDIUM,
        MeridianType.HAND_SHAOYANG_TRIPLE_BURNER,
        MeridianType.FOOT_SHAOYANG_GALLBLADDER,
        MeridianType.FOOT_JUEYIN_LIVER,
    ]

    def __init__(self):
        self.channels: Dict[str, MeridianChannel] = {}
        self.type_to_channel: Dict[MeridianType, str] = {}
        self.flow_history: List[EnergyFlowResult] = []
        self.blockage_history: List[BlockageInfo] = []
        self.total_energy: float = 1000.0
        self.network_balance: float = 1.0
        self._initialized: bool = False

    def initialize(self) -> Dict[str, Any]:
        """初始化经络网络"""
        self._initialize_twelve_regular()
        self._initialize_eight_extraordinary()
        self._establish_connections()
        self._initialized = True

        return {
            "status": "initialized",
            "total_channels": len(self.channels),
            "regular_channels": len(MeridianType.get_twelve_regular()),
            "extraordinary_channels": len(MeridianType.get_eight_extraordinary()),
            "total_energy": self.total_energy,
        }

    def _initialize_twelve_regular(self) -> None:
        """初始化十二正经"""
        regular_configs = [
            {
                "type": MeridianType.HAND_TAIYIN_LUNG,
                "name": "手太阴肺经",
                "connected_organs": ["肺"],
                "connected_modules": ["呼吸系统", "皮肤系统"],
                "active_hours": (3, 5),
                "acupoints": ["中府", "云门", "天府", "侠白", "尺泽", "孔最", "列缺", "经渠", "太渊", "鱼际", "少商"],
            },
            {
                "type": MeridianType.HAND_JUEYIN_PERICARDIUM,
                "name": "手厥阴心包经",
                "connected_organs": ["心包"],
                "connected_modules": ["心血管系统", "情绪调节"],
                "active_hours": (19, 21),
                "acupoints": ["天池", "天泉", "曲泽", "郄门", "间使", "内关", "大陵", "劳宫", "中冲"],
            },
            {
                "type": MeridianType.HAND_SHAOYIN_HEART,
                "name": "手少阴心经",
                "connected_organs": ["心"],
                "connected_modules": ["思维系统", "神明系统"],
                "active_hours": (11, 13),
                "acupoints": ["极泉", "青灵", "少海", "灵道", "通里", "阴郄", "神门", "少府", "少冲"],
            },
            {
                "type": MeridianType.HAND_YANGMING_LARGE_INTESTINE,
                "name": "手阳明大肠经",
                "connected_organs": ["大肠"],
                "connected_modules": ["排泄系统", "消化辅助"],
                "active_hours": (5, 7),
                "acupoints": ["商阳", "二间", "三间", "合谷", "阳溪", "偏历", "温溜", "下廉", "上廉", "手三里", "曲池"],
            },
            {
                "type": MeridianType.HAND_SHAOYANG_TRIPLE_BURNER,
                "name": "手少阳三焦经",
                "connected_organs": ["三焦"],
                "connected_modules": ["水液代谢", "气化系统"],
                "active_hours": (21, 23),
                "acupoints": ["关冲", "液门", "中渚", "阳池", "外关", "支沟", "会宗", "三阳络", "四渎"],
            },
            {
                "type": MeridianType.HAND_TAIYANG_SMALL_INTESTINE,
                "name": "手太阳小肠经",
                "connected_organs": ["小肠"],
                "connected_modules": ["营养吸收", "分清泌浊"],
                "active_hours": (13, 15),
                "acupoints": ["少泽", "前谷", "后溪", "腕骨", "阳谷", "养老", "支正", "小海"],
            },
            {
                "type": MeridianType.FOOT_TAIYIN_SPLEEN,
                "name": "足太阴脾经",
                "connected_organs": ["脾"],
                "connected_modules": ["消化系统", "运化系统"],
                "active_hours": (9, 11),
                "acupoints": ["隐白", "大都", "太白", "公孙", "商丘", "三阴交", "漏谷", "地机", "阴陵泉"],
            },
            {
                "type": MeridianType.FOOT_JUEYIN_LIVER,
                "name": "足厥阴肝经",
                "connected_organs": ["肝"],
                "connected_modules": ["疏泄系统", "情志调节"],
                "active_hours": (1, 3),
                "acupoints": ["大敦", "行间", "太冲", "中封", "蠡沟", "中都", "膝关", "曲泉", "阴包"],
            },
            {
                "type": MeridianType.FOOT_SHAOYIN_KIDNEY,
                "name": "足少阴肾经",
                "connected_organs": ["肾"],
                "connected_modules": ["生殖系统", "先天之本"],
                "active_hours": (17, 19),
                "acupoints": ["涌泉", "然谷", "太溪", "大钟", "水泉", "照海", "复溜", "交信", "筑宾"],
            },
            {
                "type": MeridianType.FOOT_YANGMING_STOMACH,
                "name": "足阳明胃经",
                "connected_organs": ["胃"],
                "connected_modules": ["受纳系统", "腐熟水谷"],
                "active_hours": (7, 9),
                "acupoints": ["承泣", "四白", "地仓", "大迎", "颊车", "下关", "头维", "人迎", "水突"],
            },
            {
                "type": MeridianType.FOOT_SHAOYANG_GALLBLADDER,
                "name": "足少阳胆经",
                "connected_organs": ["胆"],
                "connected_modules": ["决断系统", "少阳枢机"],
                "active_hours": (23, 1),
                "acupoints": ["瞳子髎", "听会", "上关", "颔厌", "悬颅", "悬厘", "曲鬓", "率谷"],
            },
            {
                "type": MeridianType.FOOT_TAIYANG_BLADDER,
                "name": "足太阳膀胱经",
                "connected_organs": ["膀胱"],
                "connected_modules": ["津液代谢", "卫外功能"],
                "active_hours": (15, 17),
                "acupoints": ["睛明", "攒竹", "眉冲", "曲差", "五处", "承光", "通天", "络却"],
            },
        ]

        for config in regular_configs:
            channel_id = f"meridian_{config['type'].name.lower()}"
            channel = MeridianChannel(
                channel_id=channel_id,
                name=config["name"],
                meridian_type=config["type"],
                connected_organs=config["connected_organs"],
                connected_modules=config["connected_modules"],
                active_hours=config["active_hours"],
                acupoints=config["acupoints"],
            )
            self.channels[channel_id] = channel
            self.type_to_channel[config["type"]] = channel_id

    def _initialize_eight_extraordinary(self) -> None:
        """初始化奇经八脉"""
        extraordinary_configs = [
            {
                "type": MeridianType.REN_MAI,
                "name": "任脉",
                "connected_organs": ["胞宫"],
                "connected_modules": ["阴脉之海", "调节月经", "养胎"],
                "acupoints": ["会阴", "曲骨", "中极", "关元", "石门", "气海", "阴交", "神阙"],
            },
            {
                "type": MeridianType.DU_MAI,
                "name": "督脉",
                "connected_organs": ["脑", "脊髓"],
                "connected_modules": ["阳脉之海", "总督一身之阳"],
                "acupoints": ["长强", "腰俞", "腰阳关", "命门", "悬枢", "脊中", "中枢", "筋缩"],
            },
            {
                "type": MeridianType.CHONG_MAI,
                "name": "冲脉",
                "connected_organs": ["肾", "胞宫"],
                "connected_modules": ["十二经脉之海", "血海"],
                "acupoints": ["会阴", "气冲", "横骨", "大赫", "气穴", "四满", "中注", "肓俞"],
            },
            {
                "type": MeridianType.DAI_MAI,
                "name": "带脉",
                "connected_organs": ["肾", "胞宫"],
                "connected_modules": ["约束诸经", "固护下焦"],
                "acupoints": ["带脉", "五枢", "维道", "居髎"],
            },
            {
                "type": MeridianType.YIN_QIAO_MAI,
                "name": "阴跷脉",
                "connected_organs": ["肾"],
                "connected_modules": ["调节下肢运动", "司眼睑开合"],
                "acupoints": ["照海", "交信", "睛明"],
            },
            {
                "type": MeridianType.YANG_QIAO_MAI,
                "name": "阳跷脉",
                "connected_organs": ["膀胱"],
                "connected_modules": ["调节下肢运动", "司眼睑开合"],
                "acupoints": ["申脉", "仆参", "跗阳", "居髎"],
            },
            {
                "type": MeridianType.YIN_WEI_MAI,
                "name": "阴维脉",
                "connected_organs": ["脾", "肝", "肾"],
                "connected_modules": ["维系诸阴经"],
                "acupoints": ["筑宾", "府舍", "大横", "腹哀", "期门", "天突", "廉泉"],
            },
            {
                "type": MeridianType.YANG_WEI_MAI,
                "name": "阳维脉",
                "connected_organs": ["胆", "膀胱"],
                "connected_modules": ["维系诸阳经"],
                "acupoints": ["金门", "阳交", "臑俞", "天髎", "肩井", "头维"],
            },
        ]

        for config in extraordinary_configs:
            channel_id = f"meridian_{config['type'].name.lower()}"
            channel = MeridianChannel(
                channel_id=channel_id,
                name=config["name"],
                meridian_type=config["type"],
                connected_organs=config["connected_organs"],
                connected_modules=config["connected_modules"],
                acupoints=config["acupoints"],
            )
            self.channels[channel_id] = channel
            self.type_to_channel[config["type"]] = channel_id

    def _establish_connections(self) -> None:
        """建立经络之间的连接关系"""
        yin_yang_pairs = [
            (MeridianType.HAND_TAIYIN_LUNG, MeridianType.HAND_YANGMING_LARGE_INTESTINE),
            (MeridianType.HAND_JUEYIN_PERICARDIUM, MeridianType.HAND_SHAOYANG_TRIPLE_BURNER),
            (MeridianType.HAND_SHAOYIN_HEART, MeridianType.HAND_TAIYANG_SMALL_INTESTINE),
            (MeridianType.FOOT_TAIYIN_SPLEEN, MeridianType.FOOT_YANGMING_STOMACH),
            (MeridianType.FOOT_JUEYIN_LIVER, MeridianType.FOOT_SHAOYANG_GALLBLADDER),
            (MeridianType.FOOT_SHAOYIN_KIDNEY, MeridianType.FOOT_TAIYANG_BLADDER),
        ]

        for yin_type, yang_type in yin_yang_pairs:
            yin_id = self.type_to_channel[yin_type]
            yang_id = self.type_to_channel[yang_type]
            self.channels[yin_id].add_connected_channel(yang_id)
            self.channels[yang_id].add_connected_channel(yin_id)

        for i in range(len(self.TWELVE_REGULAR_FLOW_ORDER)):
            current_type = self.TWELVE_REGULAR_FLOW_ORDER[i]
            next_type = self.TWELVE_REGULAR_FLOW_ORDER[(i + 1) % len(self.TWELVE_REGULAR_FLOW_ORDER)]
            current_id = self.type_to_channel[current_type]
            next_id = self.type_to_channel[next_type]
            self.channels[current_id].add_connected_channel(next_id)
            self.channels[next_id].add_connected_channel(current_id)

        ren_id = self.type_to_channel[MeridianType.REN_MAI]
        du_id = self.type_to_channel[MeridianType.DU_MAI]
        chong_id = self.type_to_channel[MeridianType.CHONG_MAI]
        dai_id = self.type_to_channel[MeridianType.DAI_MAI]

        for meridian_type in MeridianType.get_twelve_regular():
            if meridian_type.is_yin():
                self.channels[ren_id].add_connected_channel(self.type_to_channel[meridian_type])
            else:
                self.channels[du_id].add_connected_channel(self.type_to_channel[meridian_type])

        self.channels[ren_id].add_connected_channel(du_id)
        self.channels[du_id].add_connected_channel(ren_id)
        self.channels[chong_id].add_connected_channel(ren_id)
        self.channels[chong_id].add_connected_channel(du_id)

    def flow_energy(
        self,
        source_id: str,
        target_id: str,
        energy_amount: float
    ) -> EnergyFlowResult:
        """能量流动"""
        if source_id not in self.channels or target_id not in self.channels:
            return EnergyFlowResult(
                source_channel=source_id,
                target_channel=target_id,
                energy_amount=energy_amount,
                actual_transferred=0.0,
                flow_rate=0.0,
                blockage_encountered=True,
            )

        source = self.channels[source_id]
        target = self.channels[target_id]

        effective_flow = source.effective_flow_rate
        blockage_encountered = source.is_blocked() or target.is_blocked()

        if blockage_encountered:
            effective_flow *= (1.0 - max(source.blockage_level, target.blockage_level) * 0.5)

        actual_transferred = source.transmit_energy(energy_amount)
        actual_transferred *= effective_flow
        received = target.receive_energy(actual_transferred)

        result = EnergyFlowResult(
            source_channel=source_id,
            target_channel=target_id,
            energy_amount=energy_amount,
            actual_transferred=received,
            flow_rate=effective_flow,
            blockage_encountered=blockage_encountered,
        )

        self.flow_history.append(result)
        if len(self.flow_history) > 1000:
            self.flow_history = self.flow_history[-1000:]

        return result

    def circulate_energy(self, cycles: int = 1) -> Dict[str, Any]:
        """循环能量 - 按十二正经流注顺序循环"""
        if not self._initialized:
            return {"error": "Network not initialized"}

        results = {
            "cycles": cycles,
            "flows": [],
            "total_transferred": 0.0,
            "blockages_encountered": 0,
        }

        for _ in range(cycles):
            for i in range(len(self.TWELVE_REGULAR_FLOW_ORDER)):
                current_type = self.TWELVE_REGULAR_FLOW_ORDER[i]
                next_type = self.TWELVE_REGULAR_FLOW_ORDER[(i + 1) % len(self.TWELVE_REGULAR_FLOW_ORDER)]

                current_id = self.type_to_channel[current_type]
                next_id = self.type_to_channel[next_type]

                current_channel = self.channels[current_id]
                energy_to_flow = current_channel.current_energy * 0.1

                flow_result = self.flow_energy(current_id, next_id, energy_to_flow)
                results["flows"].append({
                    "from": current_channel.name,
                    "to": self.channels[next_id].name,
                    "transferred": flow_result.actual_transferred,
                    "blocked": flow_result.blockage_encountered,
                })
                results["total_transferred"] += flow_result.actual_transferred

                if flow_result.blockage_encountered:
                    results["blockages_encountered"] += 1

        return results

    def detect_blockage(self, threshold: float = 0.3) -> List[BlockageInfo]:
        """堵塞检测"""
        blockages = []

        for channel_id, channel in self.channels.items():
            if channel.blockage_level >= threshold:
                severity = self._classify_blockage_severity(channel.blockage_level)
                suggested_actions = self._suggest_clearing_actions(channel)

                blockage_info = BlockageInfo(
                    channel_id=channel_id,
                    channel_name=channel.name,
                    blockage_level=channel.blockage_level,
                    location=channel.name,
                    severity=severity,
                    suggested_actions=suggested_actions,
                    affected_modules=channel.connected_modules.copy(),
                )
                blockages.append(blockage_info)

        self.blockage_history.extend(blockages)
        if len(self.blockage_history) > 500:
            self.blockage_history = self.blockage_history[-500:]

        return blockages

    def _classify_blockage_severity(self, blockage_level: float) -> str:
        """分类堵塞严重程度"""
        if blockage_level >= self.BLOCKAGE_THRESHOLD_HIGH:
            return "严重"
        elif blockage_level >= self.BLOCKAGE_THRESHOLD_MEDIUM:
            return "中度"
        elif blockage_level >= self.BLOCKAGE_THRESHOLD_LOW:
            return "轻度"
        return "轻微"

    def _suggest_clearing_actions(self, channel: MeridianChannel) -> List[str]:
        """建议疏通措施"""
        actions = []

        if channel.blockage_level >= self.BLOCKAGE_THRESHOLD_HIGH:
            actions.append("紧急疏通")
            actions.append("能量注入")
            actions.append("功能模块隔离")

        if channel.blockage_level >= self.BLOCKAGE_THRESHOLD_MEDIUM:
            actions.append("渐进疏通")
            actions.append("能量重新分配")

        if channel.blockage_level >= self.BLOCKAGE_THRESHOLD_LOW:
            actions.append("常规调理")
            actions.append("能量引导")

        for module in channel.connected_modules:
            actions.append(f"检查{module}状态")

        return actions

    def clear_blockage(
        self,
        channel_id: str,
        intensity: float = 0.5
    ) -> Dict[str, Any]:
        """疏通机制"""
        if channel_id not in self.channels:
            return {"success": False, "error": f"Channel {channel_id} not found"}

        channel = self.channels[channel_id]

        if channel.blockage_level <= 0:
            return {
                "success": True,
                "channel": channel.name,
                "message": "通道已通畅，无需疏通",
                "blockage_level": 0.0,
            }

        clearing_rate = self.CLEARING_BASE_RATE * intensity * (1.0 + channel.flow_rate * 0.5)

        old_blockage = channel.blockage_level
        new_blockage = max(0.0, channel.blockage_level - clearing_rate)
        channel.blockage_level = new_blockage

        flow_improvement = channel.effective_flow_rate

        return {
            "success": True,
            "channel": channel.name,
            "old_blockage_level": old_blockage,
            "new_blockage_level": new_blockage,
            "clearing_rate": clearing_rate,
            "flow_improvement": flow_improvement,
            "remaining_blockage": new_blockage,
        }

    def clear_all_blockages(self, intensity: float = 0.3) -> Dict[str, Any]:
        """疏通所有堵塞"""
        results = {
            "channels_cleared": 0,
            "total_clearing": 0.0,
            "details": [],
        }

        for channel_id, channel in self.channels.items():
            if channel.blockage_level > 0:
                result = self.clear_blockage(channel_id, intensity)
                if result["success"]:
                    results["channels_cleared"] += 1
                    results["total_clearing"] += result.get("old_blockage_level", 0) - result.get("new_blockage_level", 0)
                    results["details"].append(result)

        return results

    def route_energy(
        self,
        source_id: str,
        target_id: str,
        energy_amount: float,
        avoid_blocked: bool = True
    ) -> Dict[str, Any]:
        """重新路由能量"""
        if source_id not in self.channels or target_id not in self.channels:
            return {"success": False, "error": "Invalid channel IDs"}

        source = self.channels[source_id]
        target = self.channels[target_id]

        if target_id in source.connected_channels:
            direct_result = self.flow_energy(source_id, target_id, energy_amount)
            if not direct_result.blockage_encountered or not avoid_blocked:
                return {
                    "success": True,
                    "route_type": "direct",
                    "path": [source_id, target_id],
                    "transferred": direct_result.actual_transferred,
                    "flow_rate": direct_result.flow_rate,
                }

        path = self._find_alternative_path(source_id, target_id, avoid_blocked)

        if not path:
            return {
                "success": False,
                "error": "No available path",
                "route_type": "none",
            }

        total_transferred = energy_amount
        current_energy = energy_amount
        path_results = []

        for i in range(len(path) - 1):
            current_id = path[i]
            next_id = path[i + 1]

            flow_result = self.flow_energy(current_id, next_id, current_energy)
            path_results.append({
                "from": self.channels[current_id].name,
                "to": self.channels[next_id].name,
                "transferred": flow_result.actual_transferred,
            })

            current_energy = flow_result.actual_transferred
            total_transferred = current_energy

            if current_energy <= 0:
                break

        return {
            "success": True,
            "route_type": "alternative",
            "path": [self.channels[p].name for p in path],
            "path_ids": path,
            "transferred": total_transferred,
            "hops": len(path) - 1,
            "penalty": (len(path) - 2) * self.ENERGY_ROUTING_PENALTY * energy_amount,
            "path_details": path_results,
        }

    def _find_alternative_path(
        self,
        source_id: str,
        target_id: str,
        avoid_blocked: bool
    ) -> List[str]:
        """寻找替代路径 - BFS算法"""
        if source_id == target_id:
            return [source_id]

        visited = set()
        queue = [[source_id]]

        while queue:
            path = queue.pop(0)
            current = path[-1]

            if current in visited:
                continue

            visited.add(current)

            for neighbor_id in self.channels[current].connected_channels:
                if neighbor_id == target_id:
                    return path + [neighbor_id]

                if neighbor_id not in visited:
                    neighbor = self.channels[neighbor_id]
                    if avoid_blocked and neighbor.is_blocked():
                        continue
                    queue.append(path + [neighbor_id])

        return []

    def get_channel(self, channel_id: str) -> Optional[MeridianChannel]:
        """获取经络通道"""
        return self.channels.get(channel_id)

    def get_channel_by_type(self, meridian_type: MeridianType) -> Optional[MeridianChannel]:
        """通过类型获取经络通道"""
        channel_id = self.type_to_channel.get(meridian_type)
        if channel_id:
            return self.channels.get(channel_id)
        return None

    def get_network_state(self) -> Dict[str, Any]:
        """获取网络状态"""
        total_flow_rate = sum(c.flow_rate for c in self.channels.values())
        avg_flow_rate = total_flow_rate / len(self.channels) if self.channels else 0

        total_blockage = sum(c.blockage_level for c in self.channels.values())
        avg_blockage = total_blockage / len(self.channels) if self.channels else 0

        blocked_channels = [c.name for c in self.channels.values() if c.is_blocked()]

        return {
            "total_channels": len(self.channels),
            "average_flow_rate": avg_flow_rate,
            "average_blockage": avg_blockage,
            "blocked_channels": blocked_channels,
            "blocked_count": len(blocked_channels),
            "total_energy": sum(c.current_energy for c in self.channels.values()),
            "network_balance": self._calculate_network_balance(),
        }

    def _calculate_network_balance(self) -> float:
        """计算网络平衡度"""
        if not self.channels:
            return 1.0

        energies = [c.current_energy for c in self.channels.values()]
        avg_energy = sum(energies) / len(energies)

        if avg_energy == 0:
            return 0.0

        variance = sum((e - avg_energy) ** 2 for e in energies) / len(energies)
        max_variance = 2500

        return max(0.0, 1.0 - variance / max_variance)

    def get_module_connections(self, module_id: str) -> List[MeridianChannel]:
        """获取功能模块连接的经络"""
        connected = []
        for channel in self.channels.values():
            if module_id in channel.connected_modules:
                connected.append(channel)
        return connected

    def inject_energy(self, channel_id: str, amount: float) -> Dict[str, Any]:
        """向经络注入能量"""
        if channel_id not in self.channels:
            return {"success": False, "error": "Channel not found"}

        channel = self.channels[channel_id]
        received = channel.receive_energy(amount)

        return {
            "success": True,
            "channel": channel.name,
            "injected": amount,
            "received": received,
            "current_energy": channel.current_energy,
            "capacity_used": channel.current_energy / channel.max_capacity,
        }

    def balance_energy(self) -> Dict[str, Any]:
        """平衡网络能量"""
        energies = [(c_id, c.current_energy) for c_id, c in self.channels.items()]
        avg_energy = sum(e for _, e in energies) / len(energies) if energies else 0

        adjustments = []
        for channel_id, current_energy in energies:
            diff = avg_energy - current_energy
            if abs(diff) > 5:
                channel = self.channels[channel_id]
                if diff > 0:
                    channel.receive_energy(diff * 0.5)
                else:
                    channel.transmit_energy(abs(diff) * 0.5)
                adjustments.append({
                    "channel": channel.name,
                    "adjustment": diff * 0.5,
                })

        return {
            "average_energy": avg_energy,
            "adjustments": adjustments,
            "new_balance": self._calculate_network_balance(),
        }

    def get_meridian_flow_sequence(self) -> List[Dict[str, Any]]:
        """获取经络流注顺序"""
        sequence = []
        for i, meridian_type in enumerate(self.TWELVE_REGULAR_FLOW_ORDER):
            channel = self.get_channel_by_type(meridian_type)
            if channel:
                sequence.append({
                    "order": i + 1,
                    "name": channel.name,
                    "type": meridian_type.value,
                    "active_hours": channel.active_hours,
                    "flow_rate": channel.flow_rate,
                    "blockage_level": channel.blockage_level,
                })
        return sequence

    def diagnose(self) -> Dict[str, Any]:
        """诊断网络健康状态"""
        blockages = self.detect_blockage()
        network_state = self.get_network_state()

        critical_channels = []
        warning_channels = []
        healthy_channels = []

        for channel in self.channels.values():
            if channel.blockage_level >= self.BLOCKAGE_THRESHOLD_HIGH:
                critical_channels.append(channel.name)
            elif channel.blockage_level >= self.BLOCKAGE_THRESHOLD_LOW:
                warning_channels.append(channel.name)
            else:
                healthy_channels.append(channel.name)

        return {
            "overall_health": network_state["network_balance"],
            "average_flow_rate": network_state["average_flow_rate"],
            "average_blockage": network_state["average_blockage"],
            "critical_channels": critical_channels,
            "warning_channels": warning_channels,
            "healthy_channels": healthy_channels,
            "blockages_detected": len(blockages),
            "recommendations": self._generate_recommendations(blockages, network_state),
        }

    def _generate_recommendations(
        self,
        blockages: List[BlockageInfo],
        network_state: Dict[str, Any]
    ) -> List[str]:
        """生成调理建议"""
        recommendations = []

        if network_state["average_blockage"] > 0.3:
            recommendations.append("建议进行全身经络疏通调理")

        if network_state["average_flow_rate"] < 0.7:
            recommendations.append("建议增强能量流动，可考虑激活相关功能模块")

        severe_blockages = [b for b in blockages if b.severity == "严重"]
        if severe_blockages:
            recommendations.append(f"发现{len(severe_blockages)}条严重堵塞经络，建议优先处理")

        if network_state["network_balance"] < 0.7:
            recommendations.append("网络能量分布不均，建议进行能量平衡调节")

        if not recommendations:
            recommendations.append("经络网络状态良好，建议保持日常调理")

        return recommendations

    def reset(self) -> None:
        """重置网络"""
        for channel in self.channels.values():
            channel.flow_rate = 1.0
            channel.blockage_level = 0.0
            channel.energy_level = 1.0
            channel.current_energy = 50.0

        self.flow_history.clear()
        self.blockage_history.clear()
        self.total_energy = 1000.0
        self.network_balance = 1.0


def create_meridian_network() -> MeridianNetwork:
    """工厂函数：创建经络网络"""
    network = MeridianNetwork()
    network.initialize()
    return network
