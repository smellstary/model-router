"""
Tiangan Dizhi (Heavenly Stems and Earthly Branches) Temporal-Spatial System
天干地支时空标签系统
"""

from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
from core.types import TianganType, DizhiType, HexagramType


class TianganDizhiSystem:
    """天干地支时空标签系统"""
    
    TIANGAN_NAMES = {
        TianganType.JIA: "甲",
        TianganType.YI: "乙",
        TianganType.BING: "丙",
        TianganType.DING: "丁",
        TianganType.WU: "戊",
        TianganType.JI: "己",
        TianganType.GENG: "庚",
        TianganType.XIN: "辛",
        TianganType.REN: "壬",
        TianganType.GUI: "癸"
    }
    
    DIZHI_NAMES = {
        DizhiType.ZI: "子",
        DizhiType.CHOU: "丑",
        DizhiType.YIN: "寅",
        DizhiType.MAO: "卯",
        DizhiType.CHEN: "辰",
        DizhiType.SI: "巳",
        DizhiType.WU: "午",
        DizhiType.WEI: "未",
        DizhiType.SHEN: "申",
        DizhiType.YOU: "酉",
        DizhiType.XU: "戌",
        DizhiType.HAI: "亥"
    }
    
    WUXING_OF_DIZHI = {
        DizhiType.ZI: "水",
        DizhiType.CHOU: "土",
        DizhiType.YIN: "木",
        DizhiType.MAO: "木",
        DizhiType.CHEN: "土",
        DizhiType.SI: "火",
        DizhiType.WU: "火",
        DizhiType.WEI: "土",
        DizhiType.SHEN: "金",
        DizhiType.YOU: "金",
        DizhiType.XU: "土",
        DizhiType.HAI: "水"
    }
    
    YIN_YANG_OF_DIZHI = {
        DizhiType.ZI: "阳",
        DizhiType.CHOU: "阴",
        DizhiType.YIN: "阳",
        DizhiType.MAO: "阴",
        DizhiType.CHEN: "阳",
        DizhiType.SI: "阴",
        DizhiType.WU: "阳",
        DizhiType.WEI: "阴",
        DizhiType.SHEN: "阳",
        DizhiType.YOU: "阴",
        DizhiType.XU: "阳",
        DizhiType.HAI: "阴"
    }
    
    def __init__(self):
        self.epoch_start = datetime(1900, 1, 1)
        self.epoch_tiangan_index = 0
        self.epoch_dizhi_index = 0
    
    def get_tiangan_index(self, dt: datetime) -> int:
        """获取天干索引"""
        days_since_epoch = (dt - self.epoch_start).days
        return (self.epoch_tiangan_index + days_since_epoch) % 10
    
    def get_dizhi_index(self, dt: datetime) -> int:
        """获取地支索引"""
        days_since_epoch = (dt - self.epoch_start).days
        return (self.epoch_dizhi_index + days_since_epoch) % 12
    
    def get_tiangan(self, dt: datetime) -> TianganType:
        """获取指定时间的天干"""
        index = self.get_tiangan_index(dt)
        return list(TianganType)[index]
    
    def get_dizhi(self, dt: datetime) -> DizhiType:
        """获取指定时间的地支"""
        index = self.get_dizhi_index(dt)
        return list(DizhiType)[index]
    
    def get_ganzhi(self, dt: datetime) -> str:
        """获取干支纪年（如甲子、丙寅等）"""
        tiangan = self.get_tiangan(dt)
        dizhi = self.get_dizhi(dt)
        return f"{self.TIANGAN_NAMES[tiangan]}{self.DIZHI_NAMES[dizhi]}"
    
    def get_cycle_position(self, dt: datetime) -> Tuple[int, int]:
        """获取在60甲子循环中的位置"""
        tiangan_idx = self.get_tiangan_index(dt)
        dizhi_idx = self.get_dizhi_index(dt)
        ganzhi_position = (tiangan_idx - dizhi_idx) % 10
        return tiangan_idx, dizhi_idx
    
    def get_wuxing_of_dizhi(self, dizhi: DizhiType) -> str:
        """获取地支的五行属性"""
        return self.WUXING_OF_DIZHI.get(dizhi, "土")
    
    def get_yin_yang_of_dizhi(self, dizhi: DizhiType) -> str:
        """获取地支的阴阳属性"""
        return self.YIN_YANG_OF_DIZHI.get(dizhi, "阳")
    
    def calculate_xiyong(self, dt: datetime) -> Dict[str, str]:
        """计算日干吉凶（时辰用事）"""
        tiangan = self.get_tiangan(dt)
        dizhi = self.get_dizhi(dt)
        
        tiangan_wuxing = self._get_tiangan_wuxing(tiangan)
        dizhi_wuxing = self.get_wuxing_of_dizhi(dizhi)
        
        return {
            'gan': tiangan.value,
            'zhi': dizhi.value,
            'gan_wuxing': tiangan_wuxing,
            'zhi_wuxing': dizhi_wuxing,
            'gan_yinyang': '阳' if tiangan.index < 5 else '阴',
            'zhi_yinyang': self.get_yin_yang_of_dizhi(dizhi)
        }
    
    def _get_tiangan_wuxing(self, tiangan: TianganType) -> str:
        """获取天干的五行属性"""
        wuxing_map = {
            TianganType.JIA: "木",
            TianganType.YI: "木",
            TianganType.BING: "火",
            TianganType.DING: "火",
            TianganType.WU: "土",
            TianganType.JI: "土",
            TianganType.GENG: "金",
            TianganType.XIN: "金",
            TianganType.REN: "水",
            TianganType.GUI: "水"
        }
        return wuxing_map.get(tiangan, "土")
    
    def suggest_memory_storage_time(self, content_type: str) -> datetime:
        """建议记忆存储时间（基于五行生克）"""
        current = datetime.now()
        tiangan = self.get_tiangan(current)
        wuxing = self._get_tiangan_wuxing(tiangan)
        
        return current
    
    def calculate_cycle_strength(self, dt: datetime) -> float:
        """计算时辰力量（0.0~1.0）"""
        dizhi = self.get_dizhi(dt)
        
        strength_map = {
            DizhiType.ZI: 1.0,
            DizhiType.CHOU: 0.6,
            DizhiType.YIN: 0.9,
            DizhiType.MAO: 0.5,
            DizhiType.CHEN: 0.7,
            DizhiType.SI: 0.8,
            DizhiType.WU: 1.0,
            DizhiType.WEI: 0.6,
            DizhiType.SHEN: 0.9,
            DizhiType.YOU: 0.5,
            DizhiType.XU: 0.7,
            DizhiType.HAI: 0.8
        }
        
        return strength_map.get(dizhi, 0.5)
    
    def get_temporal_context(self, dt: datetime) -> Dict[str, any]:
        """获取时间背景上下文"""
        return {
            'datetime': dt.isoformat(),
            'ganzhi': self.get_ganzhi(dt),
            'tiangan': self.get_tiangan(dt).value,
            'dizhi': self.get_dizhi(dt).value,
            'gan_wuxing': self._get_tiangan_wuxing(self.get_tiangan(dt)),
            'zhi_wuxing': self.get_wuxing_of_dizhi(self.get_dizhi(dt)),
            'gan_yinyang': '阳' if self.get_tiangan_index(dt) < 5 else '阴',
            'zhi_yinyang': self.get_yin_yang_of_dizhi(self.get_dizhi(dt)),
            'cycle_strength': self.calculate_cycle_strength(dt),
            'xiyong': self.calculate_xiyong(dt)
        }
    
    def match_time_pattern(
        self,
        pattern_tiangan: Optional[List[TianganType]],
        pattern_dizhi: Optional[List[DizhiType]]
    ) -> bool:
        """匹配时间模式"""
        current = datetime.now()
        current_tiangan = self.get_tiangan(current)
        current_dizhi = self.get_dizhi(current)
        
        if pattern_tiangan and current_tiangan not in pattern_tiangan:
            return False
        if pattern_dizhi and current_dizhi not in pattern_dizhi:
            return False
        
        return True
    
    def find_next_auspicious_time(
        self,
        wuxing_preference: Optional[str] = None,
        max_wait_hours: int = 24
    ) -> datetime:
        """查找下一个吉时"""
        current = datetime.now()
        
        for hour in range(max_wait_hours):
            check_time = current + timedelta(hours=hour)
            tiangan = self.get_tiangan(check_time)
            wuxing = self._get_tiangan_wuxing(tiangan)
            
            if wuxing_preference is None or wuxing == wuxing_preference:
                return check_time
        
        return current
    
    def get_bashou_analysis(self) -> Dict[str, str]:
        """获取八卦时辰分析"""
        current = datetime.now()
        dizhi = self.get_dizhi(current)
        wuxing = self.get_wuxing_of_dizhi(dizhi)
        
        analysis_map = {
            DizhiType.ZI: "坎卦，水旺，主智慧流动",
            DizhiType.CHOU: "艮卦，土旺，主积累稳固",
            DizhiType.YIN: "艮卦起始，木气初生",
            DizhiType.MAO: "震卦，木旺，主生发活动",
            DizhiType.CHEN: "巽卦，土中木旺，主变化",
            DizhiType.SI: "巽卦，火之母，主柔顺",
            DizhiType.WU: "离卦，火旺，主光明显现",
            DizhiType.WEI: "坤卦，土旺，主包容承载",
            DizhiType.SHEN: "坤卦，金始生，主刚决",
            DizhiType.YOU: "兑卦，金旺，主和谐喜悦",
            DizhiType.XU: "乾卦，土中金旺，主刚健",
            DizhiType.HAI: "乾卦，水之终，主智慧"
        }
        
        return {
            'dizhi': dizhi.value,
            'wuxing': wuxing,
            'analysis': analysis_map.get(dizhi, "综合分析")
        }
