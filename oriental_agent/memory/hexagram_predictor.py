"""
Hexagram Prediction Model (Tui Bei Tu inspired)
推背图序列预测模型

优化内容：
1. 修复转换矩阵初始化 bug
2. 新增 MarkovChainPredictor（1/2/3阶马尔可夫链）
3. 新增 TianganDizhiPredictor（天干地支时序预测）
4. 新增 EnsemblePredictor（集成预测引擎）
5. 新增 PredictionEvaluator（回测与评估）
6. 升级 TuibeituSequencePredictor（集成引擎 + 置信度 + 回测）
"""

from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
from collections import defaultdict
import math
import copy

from core.types import HexagramType, MemoryNode, WuxingType


# ============================================================================
# 常量定义
# ============================================================================

# 十天干
TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

# 十二地支
DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 天干-五行映射
TIAN_GAN_WUXING = {
    '甲': '木', '乙': '木',
    '丙': '火', '丁': '火',
    '戊': '土', '己': '土',
    '庚': '金', '辛': '金',
    '壬': '水', '癸': '水',
}

# 地支-五行映射
DI_ZHI_WUXING = {
    '子': '水', '丑': '土', '寅': '木', '卯': '木',
    '辰': '土', '巳': '火', '午': '火', '未': '土',
    '申': '金', '酉': '金', '戌': '土', '亥': '水',
}

# 地支-八卦对应（地支藏干主气对应八卦）
DI_ZHI_HEXAGRAM = {
    '子': HexagramType.KAN,   # 子水 → 坎
    '丑': HexagramType.KUN,   # 丑土 → 坤
    '寅': HexagramType.ZHEN,  # 寅木 → 震
    '卯': HexagramType.XUN,   # 卯木 → 巽
    '辰': HexagramType.KUN,   # 辰土 → 坤
    '巳': HexagramType.LI,    # 巳火 → 离
    '午': HexagramType.LI,    # 午火 → 离
    '未': HexagramType.KUN,   # 未土 → 坤
    '申': HexagramType.DUI,   # 申金 → 兑
    '酉': HexagramType.DUI,   # 酉金 → 兑
    '戌': HexagramType.GEN,   # 戌土 → 艮
    '亥': HexagramType.KAN,   # 亥水 → 坎
}

# 六十甲子表（天干地支组合循环）
def _build_sexagenary_cycle() -> List[Tuple[str, str]]:
    """构建六十甲子循环表"""
    cycle = []
    for i in range(60):
        tg = TIAN_GAN[i % 10]
        dz = DI_ZHI[i % 12]
        cycle.append((tg, dz))
    return cycle

SIXTY_CYCLE = _build_sexagenary_cycle()


class HexagramTransitionModel:
    """八卦转换模型 - 基于易经卦变原理"""

    HEXAGRAM_SYMBOLS = {
        '☰': HexagramType.QIAN,    # 乾
        '☷': HexagramType.KUN,    # 坤
        '☳': HexagramType.ZHEN,   # 震
        '☴': HexagramType.XUN,    # 巽
        '☵': HexagramType.KAN,    # 坎
        '☲': HexagramType.LI,     # 离
        '☶': HexagramType.GEN,    # 艮
        '☱': HexagramType.DUI     # 兑
    }

    TRIGRAMS_TRIGRAM_MAP = {
        HexagramType.QIAN: [1, 1, 1],
        HexagramType.KUN: [0, 0, 0],
        HexagramType.ZHEN: [0, 0, 1],
        HexagramType.XUN: [1, 0, 0],
        HexagramType.KAN: [0, 1, 0],
        HexagramType.LI: [1, 0, 1],
        HexagramType.GEN: [0, 1, 1],
        HexagramType.DUI: [1, 1, 0]
    }

    # 传统先天八卦序（伏羲八卦序）的转换关系：
    # 乾→兑→离→震→巽→坎→艮→坤→乾（循环）
    TRADITIONAL_TRANSITIONS = {
        HexagramType.QIAN: HexagramType.DUI,
        HexagramType.DUI: HexagramType.LI,
        HexagramType.LI: HexagramType.ZHEN,
        HexagramType.ZHEN: HexagramType.XUN,
        HexagramType.XUN: HexagramType.KAN,
        HexagramType.KAN: HexagramType.GEN,
        HexagramType.GEN: HexagramType.KUN,
        HexagramType.KUN: HexagramType.QIAN
    }

    def __init__(self):
        self.transition_matrix: Dict[HexagramType, Dict[HexagramType, float]] = {}
        self.memory_sequences: List[List[str]] = []
        self.sequence_patterns: Dict[str, int] = {}
        self._transition_counts: Dict[HexagramType, Dict[HexagramType, int]] = {}
        self._initialize_transition_matrix()

    def _initialize_transition_matrix(self) -> None:
        """初始化转换矩阵

        修复原 bug：原代码 source == TRADITIONAL_TRANSITIONS.get(source) 永远为 False，
        导致传统转换逻辑完全失效。

        修复方案：
        1. 以传统卦变为先验基础，给传统转换目标较高的先验概率（0.4）
        2. 其余卦象平分剩余概率（0.6 / 7）
        3. 使用拉普拉斯平滑初始化计数
        """
        all_hexagrams = list(HexagramType)
        n = len(all_hexagrams)  # 8

        for source in all_hexagrams:
            self.transition_matrix[source] = {}
            self._transition_counts[source] = {}

            # 传统转换目标
            traditional_target = self.TRADITIONAL_TRANSITIONS.get(source)

            for target in all_hexagrams:
                if target == traditional_target:
                    # 传统转换目标赋予较高先验概率
                    self.transition_matrix[source][target] = 0.4
                else:
                    # 其余卦象平分
                    self.transition_matrix[source][target] = 0.6 / (n - 1)

                # 初始化计数（拉普拉斯平滑，α=1）
                self._transition_counts[source][target] = 1

    def update_transition(self, from_hex: HexagramType, to_hex: HexagramType) -> None:
        """基于观测数据更新转换概率（增量式贝叶斯更新）"""
        if to_hex not in self.transition_matrix[from_hex]:
            return

        # 增加观测计数
        self._transition_counts[from_hex][to_hex] = \
            self._transition_counts[from_hex].get(to_hex, 0) + 1

        # 基于计数重新计算概率（狄利克雷后验估计）
        total = sum(self._transition_counts[from_hex].values())
        for hex_type in self.transition_matrix[from_hex]:
            count = self._transition_counts[from_hex][hex_type]
            self.transition_matrix[from_hex][hex_type] = count / total

    def predict_next(
        self,
        current: HexagramType,
        context: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[HexagramType, float]]:
        """预测下一个最可能的卦象"""
        if current not in self.transition_matrix:
            return []

        base_probs = self.transition_matrix[current].copy()

        if context:
            context_wuxing = context.get('wuxing')
            if context_wuxing:
                base_probs = self._apply_context_adjustment(base_probs, context_wuxing)

        predictions = sorted(base_probs.items(), key=lambda x: x[1], reverse=True)
        return predictions[:3]

    def _apply_context_adjustment(
        self,
        probs: Dict[HexagramType, float],
        context_wuxing: str
    ) -> Dict[HexagramType, float]:
        """根据五行上下文调整概率"""
        wuxing_hexagram_map = {
            '木': [HexagramType.ZHEN, HexagramType.XUN],
            '火': [HexagramType.LI],
            '土': [HexagramType.KUN, HexagramType.GEN],
            '金': [HexagramType.QIAN, HexagramType.DUI],
            '水': [HexagramType.KAN]
        }

        relevant_hexagrams = wuxing_hexagram_map.get(context_wuxing, [])

        adjusted = probs.copy()
        # 提升相关卦象的概率权重
        for hex_type in relevant_hexagrams:
            if hex_type in adjusted:
                adjusted[hex_type] *= 1.2

        # 归一化
        total = sum(adjusted.values())
        if total > 0:
            for hex_type in adjusted:
                adjusted[hex_type] /= total

        return adjusted

    def record_sequence(self, sequence: List[str]) -> None:
        """记录卦象序列，更新转换矩阵和模式统计"""
        if len(sequence) >= 2:
            for i in range(len(sequence) - 1):
                try:
                    from_hex = HexagramType(sequence[i])
                    to_hex = HexagramType(sequence[i + 1])
                    self.update_transition(from_hex, to_hex)
                except ValueError:
                    pass

            # 记录2-gram 和 3-gram 模式
            for ngram_len in [2, 3]:
                if len(sequence) >= ngram_len:
                    pattern_key = ''.join(sequence[-ngram_len:])
                    self.sequence_patterns[pattern_key] = \
                        self.sequence_patterns.get(pattern_key, 0) + 1

    def detect_sequence_pattern(self, current: HexagramType) -> Optional[str]:
        """检测序列模式并预测"""
        predictions = self.predict_next(current)
        if predictions:
            return predictions[0][0].value
        return None


# ============================================================================
# 马尔可夫链预测器（新增）
# ============================================================================

class MarkovChainPredictor:
    """多阶马尔可夫链预测器

    支持1阶、2阶、3阶马尔可夫链，根据历史数据量自动选择最优阶数。
    使用拉普拉斯平滑避免零概率问题。
    支持上下文条件化的转移概率。
    """

    def __init__(self):
        # 各阶的转移计数：order -> (context_tuple -> {next_hex -> count})
        self.transition_counts: Dict[int, Dict[Tuple, Dict[HexagramType, int]]] = {
            1: defaultdict(lambda: defaultdict(int)),
            2: defaultdict(lambda: defaultdict(int)),
            3: defaultdict(lambda: defaultdict(int)),
        }
        # 各阶的训练样本量
        self.order_samples: Dict[int, int] = {1: 0, 2: 0, 3: 0}
        # 最优阶数缓存
        self._best_order: Optional[int] = None
        # 拉普拉斯平滑参数
        self.alpha = 1.0

    def train(self, sequences: List[List[str]], max_order: int = 3) -> None:
        """从历史序列数据训练各阶马尔可夫链

        Args:
            sequences: 卦象序列列表，每个序列为 HexagramType.value 字符串列表
            max_order: 最大阶数（1/2/3）
        """
        all_hexagrams = list(HexagramType)

        for seq in sequences:
            if len(seq) < 2:
                continue

            # 转换为 HexagramType
            try:
                hex_seq = [HexagramType(s) for s in seq]
            except ValueError:
                continue

            for order in range(1, max_order + 1):
                for i in range(order, len(hex_seq)):
                    context = tuple(h.value for h in hex_seq[i - order:i])
                    next_hex = hex_seq[i]
                    self.transition_counts[order][context][next_hex] += 1
                    self.order_samples[order] += 1

        # 清除最优阶数缓存，重新选择
        self._best_order = None

    def _select_best_order(self) -> int:
        """自动选择最优马尔可夫链阶数

        选择策略：
        - 数据量 < 20：1阶（参数少，不易过拟合）
        - 20 <= 数据量 < 100：2阶
        - 数据量 >= 100：3阶（有足够数据支撑高阶模型）
        """
        if self._best_order is not None:
            return self._best_order

        # 检查各阶是否有足够样本
        for order in [3, 2, 1]:
            if self.order_samples[order] >= self._min_samples_for_order(order):
                self._best_order = order
                return order

        # 降级到1阶
        self._best_order = 1
        return 1

    @staticmethod
    def _min_samples_for_order(order: int) -> int:
        """各阶所需最小样本量（基于参数数量估算）"""
        n_states = len(HexagramType)  # 8
        # n_states^order 个上下文，每个上下文至少应有几个样本
        min_per_context = 3
        return n_states ** order * min_per_context

    def predict(
        self,
        history: List[str],
        context: Optional[Dict[str, Any]] = None,
        top_k: int = 3
    ) -> List[Tuple[HexagramType, float]]:
        """基于历史序列预测下一个卦象

        Args:
            history: 历史卦象序列（value 字符串列表），最近的在最后
            context: 可选上下文（如五行信息）
            top_k: 返回 top-k 预测

        Returns:
            [(HexagramType, probability), ...] 按概率降序排列
        """
        order = self._select_best_order()

        # 尝试用最高可用阶数，逐渐降级
        available_history = list(history[-(order):]) if len(history) >= order else list(history)
        actual_order = len(available_history)

        if actual_order < 1:
            # 无历史数据，返回均匀分布
            return [(h, 1.0 / len(HexagramType)) for h in HexagramType][:top_k]

        # 使用实际可用的阶数
        use_order = min(actual_order, order)
        context_tuple = tuple(available_history[-use_order:])

        counts = self.transition_counts[use_order].get(context_tuple, {})
        total_count = sum(counts.values())

        all_hexagrams = list(HexagramType)

        if total_count == 0:
            # 该上下文无观测数据，降级到更低阶
            if use_order > 1:
                # 去掉最远的一个历史，用少一阶的上下文
                shorter_history = list(history[-(use_order - 1):]) if use_order > 1 else []
                if shorter_history:
                    return self.predict(shorter_history, context, top_k)
            # 最终降级：返回传统卦变先验
            return self._traditional_prior_prediction(top_k)

        # 拉普拉斯平滑概率估计
        n_states = len(all_hexagrams)
        smoothed_probs = {}
        for hex_type in all_hexagrams:
            count = counts.get(hex_type, 0)
            smoothed_probs[hex_type] = (count + self.alpha) / (total_count + self.alpha * n_states)

        # 应用上下文调整
        if context and context.get('wuxing'):
            smoothed_probs = self._apply_context_adjustment(smoothed_probs, context['wuxing'])

        predictions = sorted(smoothed_probs.items(), key=lambda x: x[1], reverse=True)
        return predictions[:top_k]

    def _traditional_prior_prediction(self, top_k: int) -> List[Tuple[HexagramType, float]]:
        """返回基于传统卦变的先验预测（无数据时的回退方案）"""
        model = HexagramTransitionModel()
        # 取任意卦的传统转换（这里取乾卦作为基准）
        return model.predict_next(HexagramType.QIAN)[:top_k]

    def _apply_context_adjustment(
        self,
        probs: Dict[HexagramType, float],
        context_wuxing: str
    ) -> Dict[HexagramType, float]:
        """五行上下文调整（同 HexagramTransitionModel）"""
        wuxing_hexagram_map = {
            '木': [HexagramType.ZHEN, HexagramType.XUN],
            '火': [HexagramType.LI],
            '土': [HexagramType.KUN, HexagramType.GEN],
            '金': [HexagramType.QIAN, HexagramType.DUI],
            '水': [HexagramType.KAN]
        }
        relevant = wuxing_hexagram_map.get(context_wuxing, [])
        adjusted = probs.copy()
        for h in relevant:
            if h in adjusted:
                adjusted[h] *= 1.2
        total = sum(adjusted.values())
        if total > 0:
            for h in adjusted:
                adjusted[h] /= total
        return adjusted

    def predict_multi_step(
        self,
        history: List[str],
        steps: int = 3,
        context: Optional[Dict[str, Any]] = None
    ) -> List[Dict]:
        """多步预测，返回每步的 top-1 预测及置信度衰减

        Args:
            history: 历史卦象序列
            steps: 预测步数
            context: 上下文

        Returns:
            每步预测结果列表，包含卦象、概率、置信度衰减系数
        """
        results = []
        current_history = list(history)

        for step in range(steps):
            predictions = self.predict(current_history, context, top_k=1)
            if predictions:
                next_hex, prob = predictions[0]
                # 置信度随步数衰减
                confidence_decay = 0.85 ** step
                results.append({
                    'hexagram': next_hex.value,
                    'hexagram_type': next_hex,
                    'probability': prob,
                    'step': step + 1,
                    'confidence_decay': confidence_decay,
                    'adjusted_confidence': prob * confidence_decay,
                })
                current_history.append(next_hex.value)
            else:
                break

        return results


# ============================================================================
# 天干地支预测器（新增）
# ============================================================================

class TianganDizhiPredictor:
    """天干地支时序预测器

    结合天干地支时序进行周期预测：
    - 识别六十甲子周期模式
    - 根据当前时辰/年份对应的天干地支给出卦象倾向
    - 支持时辰级别的时间权重
    """

    def __init__(self):
        # 六十甲子 -> 卦象的映射（通过地支主气）
        self.cycle_hexagram_map: Dict[int, HexagramType] = {}
        self._build_cycle_map()
        # 周期模式计数：(天干索引, 地支索引) -> {卦象 -> 计数}
        self.pattern_counts: Dict[Tuple[int, int], Dict[HexagramType, int]] = defaultdict(
            lambda: defaultdict(int)
        )
        # 记录过的周期观测
        self.observations: List[Dict] = []

    def _build_cycle_map(self) -> None:
        """构建六十甲子周期卦象映射"""
        for i, (tg, dz) in enumerate(SIXTY_CYCLE):
            # 通过地支对应卦象
            self.cycle_hexagram_map[i] = DI_ZHI_HEXAGRAM[dz]

    def get_current_cycle_position(self, dt: Optional[datetime] = None) -> Dict[str, Any]:
        """获取当前时刻在六十甲子周期中的位置

        Args:
            dt: 时间，默认当前时间

        Returns:
            包含天干、地支、周期位置、对应卦象等信息
        """
        if dt is None:
            dt = datetime.now()

        # 使用年份计算天干地支（简化算法）
        year = dt.year
        # 天干索引：(年份 - 4) % 10，因为公元4年是甲子年
        tg_idx = (year - 4) % 10
        dz_idx = (year - 4) % 12
        cycle_idx = (tg_idx * 6 - dz_idx * 5) % 60  # 六十甲子位置

        tg = TIAN_GAN[tg_idx]
        dz = DI_ZHI[dz_idx]

        return {
            'year': year,
            'tiangan': tg,
            'tiangan_idx': tg_idx,
            'tiangan_wuxing': TIAN_GAN_WUXING[tg],
            'dizhi': dz,
            'dizhi_idx': dz_idx,
            'dizhi_wuxing': DI_ZHI_WUXING[dz],
            'cycle_index': cycle_idx,
            'cycle_hexagram': self.cycle_hexagram_map.get(cycle_idx),
            'hour': dt.hour,
        }

    def get_hour_weight(self, hour: Optional[int] = None) -> float:
        """计算时辰权重（子时权重最高，向午时递减再回升）

        时辰权重基于传统时辰理论：
        - 子时(23-1)：阳气初生，权重最高
        - 午时(11-13)：阳气鼎盛，权重次高
        - 卯时(5-7)、酉时(17-19)：阴阳交替，权重中等
        """
        if hour is None:
            hour = datetime.now().hour

        # 简化的时辰权重模型：以子时和午时为高峰的正弦函数
        # 子时(0点)和午时(12点)权重最高
        import math
        weight = 0.7 + 0.3 * math.cos(2 * math.pi * (hour - 12) / 24)
        return weight

    def predict(
        self,
        dt: Optional[datetime] = None,
        history_pattern: Optional[List[str]] = None,
        top_k: int = 3
    ) -> List[Tuple[HexagramType, float]]:
        """基于天干地支时序进行预测

        Args:
            dt: 预测目标时间
            history_pattern: 历史观测序列（用于学习周期模式）
            top_k: 返回 top-k

        Returns:
            [(HexagramType, probability), ...]
        """
        if dt is None:
            dt = datetime.now()

        cycle_info = self.get_current_cycle_position(dt)
        hour_weight = self.get_hour_weight(dt.hour)
        base_hex = cycle_info['cycle_hexagram']

        all_hexagrams = list(HexagramType)

        if not base_hex:
            # 退回到均匀分布
            return [(h, 1.0 / len(all_hexagrams)) for h in all_hexagrams][:top_k]

        # 基础概率分布：以周期卦象为中心
        probs = {}
        for h in all_hexagrams:
            if h == base_hex:
                probs[h] = 0.35  # 周期卦象基础概率
            else:
                # 其余卦象按与传统卦变关系的远近分配
                if h == HexagramTransitionModel.TRADITIONAL_TRANSITIONS.get(base_hex):
                    probs[h] = 0.25  # 传统转换目标
                else:
                    probs[h] = (1.0 - 0.35 - 0.25) / (len(all_hexagrams) - 2)

        # 如果有历史模式数据，用贝叶斯更新
        if history_pattern and len(history_pattern) >= 3:
            cycle_idx = cycle_info['cycle_index']
            tg_idx = cycle_info['tiangan_idx']
            dz_idx = cycle_info['dizhi_idx']

            # 检查当前天干地支组合下是否有历史观测
            key = (tg_idx, dz_idx)
            pattern_data = self.pattern_counts.get(key, {})
            pattern_total = sum(pattern_data.values())

            if pattern_total > 0:
                # 混合历史模式概率（权重随观测数量增加）
                history_weight = min(0.6, pattern_total / (pattern_total + 10))

                # 历史模式概率（拉普拉斯平滑）
                history_probs = {}
                n_states = len(all_hexagrams)
                for h in all_hexagrams:
                    count = pattern_data.get(h, 0)
                    history_probs[h] = (count + 1) / (pattern_total + n_states)

                # 混合：时序先验 + 历史模式
                for h in all_hexagrams:
                    probs[h] = (1 - history_weight) * probs[h] + history_weight * history_probs[h]

        # 应用时辰权重调整
        if hour_weight > 0.8:
            # 高权重时辰，增强周期卦象的趋势
            for h in all_hexagrams:
                if h == base_hex:
                    probs[h] *= (1 + 0.1 * hour_weight)

            # 归一化
            total = sum(probs.values())
            if total > 0:
                for h in probs:
                    probs[h] /= total

        # 五行上下文调整
        tg_wx = cycle_info['tiangan_wuxing']
        dz_wx = cycle_info['dizhi_wuxing']
        # 综合五行（天干权重0.6，地支权重0.4）
        combined_wuxing = tg_wx  # 简化处理

        wuxing_hexagram_map = {
            '木': [HexagramType.ZHEN, HexagramType.XUN],
            '火': [HexagramType.LI],
            '土': [HexagramType.KUN, HexagramType.GEN],
            '金': [HexagramType.QIAN, HexagramType.DUI],
            '水': [HexagramType.KAN]
        }
        relevant = wuxing_hexagram_map.get(combined_wuxing, [])
        for h in relevant:
            if h in probs:
                probs[h] *= 1.15

        # 最终归一化
        total = sum(probs.values())
        if total > 0:
            for h in probs:
                probs[h] /= total

        predictions = sorted(probs.items(), key=lambda x: x[1], reverse=True)
        return predictions[:top_k]

    def record_observation(
        self,
        dt: datetime,
        observed_hexagram: HexagramType
    ) -> None:
        """记录一次观测，用于学习周期模式

        Args:
            dt: 观测时间
            observed_hexagram: 观测到的卦象
        """
        cycle_info = self.get_current_cycle_position(dt)
        key = (cycle_info['tiangan_idx'], cycle_info['dizhi_idx'])
        self.pattern_counts[key][observed_hexagram] += 1
        self.observations.append({
            'time': dt,
            'hexagram': observed_hexagram.value,
            'cycle_info': cycle_info,
        })

    def get_cycle_trend(self, steps_ahead: int = 5) -> List[Dict]:
        """预测未来若干周期的趋势

        Args:
            steps_ahead: 未来多少个周期

        Returns:
            每个周期的预测信息
        """
        now = datetime.now()
        trends = []
        for i in range(1, steps_ahead + 1):
            future_dt = datetime(now.year + i, now.month, now.day)
            predictions = self.predict(future_dt)
            cycle_info = self.get_current_cycle_position(future_dt)
            if predictions:
                trends.append({
                    'year': now.year + i,
                    'tiangan': cycle_info['tiangan'],
                    'dizhi': cycle_info['dizhi'],
                    'predicted_hexagram': predictions[0][0].value,
                    'confidence': predictions[0][1],
                })
        return trends


# ============================================================================
# 集成预测器（新增）
# ============================================================================

class EnsemblePredictor:
    """集成预测引擎

    集成三种预测方法：
    1. 马尔可夫链预测器
    2. 传统卦变模型
    3. 天干地支时序预测器

    根据历史准确率动态调整权重，输出预测置信度和不确定性区间。
    """

    def __init__(self):
        self.markov = MarkovChainPredictor()
        self.traditional = HexagramTransitionModel()
        self.tiangan_dizhi = TianganDizhiPredictor()

        # 各预测器权重（初始均匀）
        self.weights = {
            'markov': 0.33,
            'traditional': 0.34,
            'tiangan_dizhi': 0.33,
        }

        # 历史表现跟踪
        self.performance: Dict[str, Dict] = {
            'markov': {'correct': 0, 'total': 0, 'accuracy': 0.0},
            'traditional': {'correct': 0, 'total': 0, 'accuracy': 0.0},
            'tiangan_dizhi': {'correct': 0, 'total': 0, 'accuracy': 0.0},
        }

        # 回测记录
        self.backtest_records: List[Dict] = []

    def train_markov(self, sequences: List[List[str]], max_order: int = 3) -> None:
        """训练马尔可夫链预测器"""
        self.markov.train(sequences, max_order)

    def record_training_data(self, sequence: List[str]) -> None:
        """记录训练数据到传统模型"""
        self.traditional.record_sequence(sequence)

    def predict(
        self,
        current: HexagramType,
        history: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None,
        top_k: int = 3,
        dt: Optional[datetime] = None,
    ) -> Dict:
        """集成预测

        Args:
            current: 当前卦象
            history: 历史序列（用于马尔可夫链和天干地支）
            context: 上下文信息（如五行）
            top_k: 返回 top-k
            dt: 预测时间（天干地支预测用）

        Returns:
            {
                'predictions': [(HexagramType, probability), ...],
                'confidence': float,  # 整体置信度
                'uncertainty': float,  # 不确定性 (熵)
                'component_predictions': {  # 各预测器的独立结果
                    'markov': [...],
                    'traditional': [...],
                    'tiangan_dizhi': [...],
                },
                'weights_used': {...},
            }
        """
        all_hexagrams = list(HexagramType)
        component_probs: Dict[str, Dict[HexagramType, float]] = {}

        # 1. 传统卦变预测
        trad_preds = self.traditional.predict_next(current, context)
        component_probs['traditional'] = {h: 0.0 for h in all_hexagrams}
        for h, p in trad_preds:
            component_probs['traditional'][h] = p

        # 2. 马尔可夫链预测
        if history and len(history) >= 1:
            markov_preds = self.markov.predict(history, context, top_k=top_k)
            component_probs['markov'] = {h: 0.0 for h in all_hexagrams}
            for h, p in markov_preds:
                component_probs['markov'][h] = p
        else:
            # 无历史数据时，退化为传统预测
            component_probs['markov'] = component_probs['traditional'].copy()

        # 3. 天干地支预测
        if history and len(history) >= 3:
            tz_preds = self.tiangan_dizhi.predict(dt, history_pattern=history, top_k=top_k)
            component_probs['tiangan_dizhi'] = {h: 0.0 for h in all_hexagrams}
            for h, p in tz_preds:
                component_probs['tiangan_dizhi'][h] = p
        else:
            # 数据不足时退化为传统预测
            component_preds = self.tiangan_dizhi.predict(dt, top_k=top_k)
            component_probs['tiangan_dizhi'] = {h: 0.0 for h in all_hexagrams}
            for h, p in component_preds:
                component_probs['tiangan_dizhi'][h] = p

        # 动态权重调整（基于历史表现）
        adjusted_weights = self._adjust_weights()

        # 加权融合
        ensemble_probs = {h: 0.0 for h in all_hexagrams}
        for name, probs in component_probs.items():
            w = adjusted_weights.get(name, 0.0)
            for h in all_hexagrams:
                ensemble_probs[h] += w * probs[h]

        # 归一化
        total = sum(ensemble_probs.values())
        if total > 0:
            for h in ensemble_probs:
                ensemble_probs[h] /= total

        # 计算置信度和不确定性
        confidence, uncertainty = self._compute_confidence(ensemble_probs)

        predictions = sorted(ensemble_probs.items(), key=lambda x: x[1], reverse=True)

        return {
            'predictions': predictions[:top_k],
            'confidence': confidence,
            'uncertainty': uncertainty,
            'component_predictions': {
                name: sorted(probs.items(), key=lambda x: x[1], reverse=True)[:top_k]
                for name, probs in component_probs.items()
            },
            'weights_used': adjusted_weights,
        }

    def predict_multi_step(
        self,
        current: HexagramType,
        history: Optional[List[str]] = None,
        steps: int = 3,
        context: Optional[Dict[str, Any]] = None,
        dt: Optional[datetime] = None,
    ) -> List[Dict]:
        """多步预测，带置信度衰减

        Args:
            current: 当前卦象
            history: 历史序列
            steps: 预测步数
            context: 上下文
            dt: 起始时间

        Returns:
            每步预测结果，包含卦象、概率、置信度衰减
        """
        results = []
        extended_history = list(history) if history else [current.value]
        current_hex = current

        for step in range(steps):
            result = self.predict(
                current=current_hex,
                history=extended_history,
                context=context,
                top_k=3,
                dt=dt,
            )

            if result['predictions']:
                next_hex, prob = result['predictions'][0]
                # 置信度随步数指数衰减
                confidence_decay = 0.85 ** step
                adjusted_confidence = result['confidence'] * confidence_decay

                results.append({
                    'step': step + 1,
                    'hexagram': next_hex.value,
                    'hexagram_type': next_hex,
                    'probability': prob,
                    'ensemble_confidence': result['confidence'],
                    'confidence_decay': confidence_decay,
                    'adjusted_confidence': adjusted_confidence,
                    'uncertainty': result['uncertainty'],
                    'weights': result['weights_used'],
                })

                extended_history.append(next_hex.value)
                current_hex = next_hex
            else:
                break

        return results

    def _adjust_weights(self) -> Dict[str, float]:
        """基于历史表现动态调整各预测器权重"""
        total_correct = sum(p['correct'] for p in self.performance.values())
        total_evaluated = sum(p['total'] for p in self.performance.values())

        if total_evaluated < 5:
            # 评估数据不足，使用初始权重
            return self.weights.copy()

        new_weights = {}
        for name, perf in self.performance.items():
            if perf['total'] > 0:
                # 基于准确率的权重（加平滑避免零权重）
                new_weights[name] = perf['accuracy'] + 0.1
            else:
                new_weights[name] = 0.1

        # 归一化
        total_w = sum(new_weights.values())
        if total_w > 0:
            for name in new_weights:
                new_weights[name] /= total_w
        else:
            new_weights = self.weights.copy()

        return new_weights

    def evaluate_prediction(
        self,
        prediction: Dict,
        actual: HexagramType
    ) -> Dict[str, bool]:
        """评估一次预测结果，更新各预测器表现统计

        Args:
            prediction: predict() 的返回结果
            actual: 实际发生的卦象

        Returns:
            各预测器是否命中
        """
        results = {}
        for name in self.performance:
            # 检查该预测器的 top-1 是否命中
            comp_preds = prediction.get('component_predictions', {}).get(name, [])
            if comp_preds:
                hit = comp_preds[0][0] == actual
                results[name] = hit
                self.performance[name]['total'] += 1
                if hit:
                    self.performance[name]['correct'] += 1

                # 更新准确率
                if self.performance[name]['total'] > 0:
                    self.performance[name]['accuracy'] = \
                        self.performance[name]['correct'] / self.performance[name]['total']

        # 检查集成预测是否命中
        preds = prediction.get('predictions', [])
        if preds:
            results['ensemble'] = preds[0][0] == actual

        return results

    @staticmethod
    def _compute_confidence(probs: Dict[HexagramType, float]) -> Tuple[float, float]:
        """计算预测置信度和不确定性（信息熵）

        Returns:
            (confidence, uncertainty)
            confidence = top-1 概率
            uncertainty = 归一化信息熵 [0, 1]
        """
        if not probs:
            return 0.0, 1.0

        # 置信度 = 最高概率
        confidence = max(probs.values())

        # 信息熵
        entropy = 0.0
        for p in probs.values():
            if p > 0:
                entropy -= p * math.log2(p)

        # 归一化熵（最大熵 = log2(n)）
        n = len(probs)
        max_entropy = math.log2(n) if n > 1 else 1.0
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0.0

        return confidence, normalized_entropy

    def get_prediction_quality(self) -> Dict[str, Any]:
        """获取当前预测质量报告"""
        report = {
            'component_performance': {},
            'overall_accuracy': 0.0,
            'total_evaluations': 0,
        }

        total_correct = 0
        total_evaluated = 0

        for name, perf in self.performance.items():
            report['component_performance'][name] = {
                'accuracy': perf['accuracy'],
                'correct': perf['correct'],
                'total': perf['total'],
            }
            total_correct += perf['correct']
            total_evaluated += perf['total']

        report['overall_accuracy'] = total_correct / total_evaluated if total_evaluated > 0 else 0.0
        report['total_evaluations'] = total_evaluated
        report['current_weights'] = self._adjust_weights()

        return report


# ============================================================================
# 预测评估器（新增）
# ============================================================================

class PredictionEvaluator:
    """预测质量评估器

    支持回测预测准确率，跟踪各预测器表现，提供预测质量报告。
    """

    def __init__(self):
        self.evaluator = EnsemblePredictor()
        self.evaluation_results: List[Dict] = []
        self.step_accuracy: Dict[int, Dict] = defaultdict(
            lambda: {'correct': 0, 'total': 0}
        )

    def backtest(
        self,
        data: List[Dict],
        window_size: int = 5
    ) -> Dict[str, Any]:
        """历史回测

        Args:
            data: 历史数据列表，每项包含：
                - 'sequence': List[str] 历史卦象序列
                - 'actual': str 实际发生的下一个卦象
                - 'timestamp': Optional[str] 时间戳（可选）
                - 'context': Optional[Dict] 上下文（可选）
            window_size: 用于预测的历史窗口大小

        Returns:
            回测报告
        """
        self.evaluation_results = []
        self.step_accuracy = defaultdict(lambda: {'correct': 0, 'total': 0})

        # 收集所有序列训练马尔可夫链
        all_sequences = [d['sequence'] for d in data if len(d['sequence']) >= 2]
        self.evaluator.train_markov(all_sequences, max_order=3)
        for seq in all_sequences:
            self.evaluator.record_training_data(seq)

        total = len(data)
        correct_top1 = 0
        correct_top3 = 0

        for i, item in enumerate(data):
            seq = item['sequence']
            actual_str = item['actual']

            try:
                actual_hex = HexagramType(actual_str)
            except ValueError:
                continue

            # 使用窗口内的历史做预测
            history = seq[-window_size:] if len(seq) >= window_size else seq
            current = HexagramType(seq[-1]) if seq else None

            if not current or not history:
                continue

            context = item.get('context')
            timestamp = item.get('timestamp')
            dt = None
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp)
                except (ValueError, TypeError):
                    pass

            prediction = self.evaluator.predict(
                current=current,
                history=history,
                context=context,
                top_k=3,
                dt=dt,
            )

            # 评估
            eval_result = self.evaluator.evaluate_prediction(prediction, actual_hex)

            if prediction['predictions']:
                top1_hex = prediction['predictions'][0][0]
                top3_hexes = [p[0] for p in prediction['predictions'][:3]]

                hit_top1 = top1_hex == actual_hex
                hit_top3 = actual_hex in top3_hexes

                if hit_top1:
                    correct_top1 += 1
                if hit_top3:
                    correct_top3 += 1

                self.evaluation_results.append({
                    'index': i,
                    'actual': actual_str,
                    'predicted_top1': top1_hex.value,
                    'predicted_top3': [p[0].value for p in prediction['predictions'][:3]],
                    'hit_top1': hit_top1,
                    'hit_top3': hit_top3,
                    'confidence': prediction['confidence'],
                    'uncertainty': prediction['uncertainty'],
                    'component_results': eval_result,
                    'weights': prediction['weights_used'],
                })

        # 生成报告
        n_evaluated = len(self.evaluation_results)
        report = {
            'total_samples': total,
            'evaluated_samples': n_evaluated,
            'top1_accuracy': correct_top1 / n_evaluated if n_evaluated > 0 else 0.0,
            'top3_accuracy': correct_top3 / n_evaluated if n_evaluated > 0 else 0.0,
            'avg_confidence': sum(r['confidence'] for r in self.evaluation_results) / n_evaluated if n_evaluated > 0 else 0.0,
            'avg_uncertainty': sum(r['uncertainty'] for r in self.evaluation_results) / n_evaluated if n_evaluated > 0 else 0.0,
            'component_performance': self.evaluator.get_prediction_quality()['component_performance'],
            'detailed_results': self.evaluation_results,
        }

        return report

    def backtest_multi_step(
        self,
        data: List[Dict],
        steps: int = 3,
        window_size: int = 5,
    ) -> Dict[str, Any]:
        """多步预测回测

        Args:
            data: 历史数据，每项包含 'sequence' 和 'future_steps'（未来实际序列）
            steps: 预测步数
            window_size: 历史窗口大小

        Returns:
            多步回测报告
        """
        step_hits: Dict[int, int] = defaultdict(int)
        step_totals: Dict[int, int] = defaultdict(int)

        all_sequences = [d['sequence'] for d in data if len(d['sequence']) >= 2]
        self.evaluator.train_markov(all_sequences, max_order=3)

        for item in data:
            seq = item['sequence']
            future = item.get('future_steps', [])

            if len(seq) < 2 or len(future) < 1:
                continue

            history = seq[-window_size:] if len(seq) >= window_size else list(seq)
            current = HexagramType(seq[-1])

            multi_preds = self.evaluator.predict_multi_step(
                current=current,
                history=history,
                steps=min(steps, len(future)),
            )

            for pred in multi_preds:
                step = pred['step']
                actual = future[step - 1] if step <= len(future) else None
                if actual:
                    step_totals[step] += 1
                    try:
                        if pred['hexagram_type'] == HexagramType(actual):
                            step_hits[step] += 1
                    except ValueError:
                        pass

        # 各步准确率
        accuracy_by_step = {}
        for step in range(1, steps + 1):
            total = step_totals.get(step, 0)
            accuracy_by_step[str(step)] = {
                'accuracy': step_hits.get(step, 0) / total if total > 0 else 0.0,
                'total': total,
                'correct': step_hits.get(step, 0),
            }

        return {
            'steps': steps,
            'accuracy_by_step': accuracy_by_step,
            'total_evaluated': sum(step_totals.values()),
        }

    def get_quality_report(self) -> Dict[str, Any]:
        """获取预测质量报告"""
        return self.evaluator.get_prediction_quality()


# ============================================================================
# 推背图序列预测器（升级）
# ============================================================================

class TuibeituSequencePredictor:
    """推背图序列预测器（升级版）

    使用 EnsemblePredictor 作为核心预测引擎，
    支持多步预测、置信度衰减、历史回测。
    """

    def __init__(self):
        # 保留原有接口
        self.hexagram_model = HexagramTransitionModel()
        self.historical_predictions: List[Dict] = []
        self.sequence_templates: Dict[str, List[str]] = {}
        self.cycle_stages = {
            0: "天地初开",
            1: "万物生发",
            2: "繁荣鼎盛",
            3: "阴阳交替",
            4: "变化孕育",
            5: "转化过渡",
            6: "新秩序立",
            7: "循环往复"
        }

        # 新增集成引擎
        self.ensemble = EnsemblePredictor()
        self.evaluator = PredictionEvaluator()

    def analyze_current_state(
        self,
        current_hexagram: HexagramType,
        memory_states: List[MemoryNode]
    ) -> Dict[str, Any]:
        """分析当前状态（向后兼容）"""
        # 使用集成引擎预测
        predictions = self.hexagram_model.predict_next(current_hexagram)

        active_wuxing = self._extract_active_wuxing(memory_states)
        context = {'wuxing': active_wuxing[0]} if active_wuxing else None

        # 同时使用集成引擎获取更丰富的预测
        ensemble_pred = self.ensemble.predict(
            current=current_hexagram,
            context=context,
        )

        return {
            'current_hexagram': current_hexagram.value,
            'predictions': [
                {'hexagram': h.value, 'probability': p}
                for h, p in predictions
            ],
            'ensemble_predictions': [
                {'hexagram': h.value, 'probability': p}
                for h, p in ensemble_pred['predictions']
            ],
            'active_wuxing': active_wuxing,
            'recommended_direction': self._suggest_direction(predictions, active_wuxing),
            'ensemble_confidence': ensemble_pred['confidence'],
            'uncertainty': ensemble_pred['uncertainty'],
        }

    def _extract_active_wuxing(self, memories: List[MemoryNode]) -> List[str]:
        """提取活跃的五行"""
        wuxing_counts = {}
        for memory in memories:
            wuxing = memory.wuxing_attribute.value
            wuxing_counts[wuxing] = wuxing_counts.get(wuxing, 0) + memory.weight

        sorted_wuxing = sorted(wuxing_counts.items(), key=lambda x: x[1], reverse=True)
        return [w for w, _ in sorted_wuxing[:3]]

    def _suggest_direction(
        self,
        predictions: List[Tuple[HexagramType, float]],
        active_wuxing: List[str]
    ) -> str:
        """建议发展方向"""
        if not predictions:
            return "维持现状"

        top_hexagram = predictions[0][0]

        hexagram_meanings = {
            HexagramType.QIAN: "刚健进取",
            HexagramType.KUN: "柔顺包容",
            HexagramType.ZHEN: "震动变革",
            HexagramType.XUN: "柔顺渗透",
            HexagramType.KAN: "陷溺危险",
            HexagramType.LI: "光明依附",
            HexagramType.GEN: "静止安稳",
            HexagramType.DUI: "喜悦和谐"
        }

        return hexagram_meanings.get(top_hexagram, "观察等待")

    def predict_sequence(
        self,
        current: HexagramType,
        steps: int = 3,
        context: Optional[Dict] = None
    ) -> List[Dict]:
        """预测序列演化（向后兼容，调用集成引擎）"""
        # 尝试从历史记录中提取历史序列
        history = self._build_history_from_predictions()

        multi_step = self.ensemble.predict_multi_step(
            current=current,
            history=history if history else None,
            steps=steps,
            context=context,
        )

        # 兼容旧格式
        return [
            {
                'hexagram': s['hexagram'],
                'probability': s['probability'],
                'stage': self._get_stage_description(s['step'] - 1),
                'confidence': s.get('adjusted_confidence', s['probability']),
                'step': s['step'],
            }
            for s in multi_step
        ]

    def predict_with_confidence(
        self,
        current: HexagramType,
        steps: int = 3,
        context: Optional[Dict] = None,
        dt: Optional[datetime] = None,
    ) -> Dict:
        """带置信度的预测（新方法）

        Args:
            current: 当前卦象
            steps: 预测步数
            context: 上下文
            dt: 预测时间

        Returns:
            {
                'sequence': [...],  # 多步预测结果
                'overall_confidence': float,
                'uncertainty': float,
                'component_predictions': {...},
            }
        """
        history = self._build_history_from_predictions()

        multi_step = self.ensemble.predict_multi_step(
            current=current,
            history=history if history else None,
            steps=steps,
            context=context,
            dt=dt,
        )

        # 整体置信度取第一步的置信度，不确定性取平均值
        overall_confidence = multi_step[0]['ensemble_confidence'] if multi_step else 0.0
        avg_uncertainty = (
            sum(s['uncertainty'] for s in multi_step) / len(multi_step)
            if multi_step else 1.0
        )

        return {
            'sequence': multi_step,
            'overall_confidence': overall_confidence,
            'uncertainty': avg_uncertainty,
            'component_predictions': (
                self.ensemble.predict(
                    current=current,
                    history=history if history else None,
                    context=context,
                    dt=dt,
                )['component_predictions']
            ),
        }

    def backtest(
        self,
        data: List[Dict],
        window_size: int = 5,
        multi_step: bool = False,
        steps: int = 3,
    ) -> Dict[str, Any]:
        """历史回测（新方法）

        Args:
            data: 回测数据
            window_size: 历史窗口大小
            multi_step: 是否进行多步回测
            steps: 多步预测步数

        Returns:
            回测报告
        """
        if multi_step:
            return self.evaluator.backtest_multi_step(
                data, steps=steps, window_size=window_size
            )
        return self.evaluator.backtest(data, window_size=window_size)

    def get_prediction_quality(self) -> Dict[str, Any]:
        """获取预测质量报告（新方法）"""
        return self.evaluator.get_quality_report()

    def _get_stage_description(self, step: int) -> str:
        """获取阶段描述"""
        stage_key = step % len(self.cycle_stages)
        return self.cycle_stages[stage_key]

    def _build_history_from_predictions(self) -> Optional[List[str]]:
        """从历史预测记录中提取历史序列"""
        if not self.historical_predictions:
            return None
        # 提取最近 20 条记录
        recent = self.historical_predictions[-20:]
        history = []
        for rec in recent:
            if isinstance(rec, dict) and 'hexagram' in rec:
                history.append(rec['hexagram'])
        return history if len(history) >= 2 else None

    def record_prediction(self, current: HexagramType, predicted: HexagramType) -> None:
        """记录一次预测结果，用于后续训练"""
        self.historical_predictions.append({
            'hexagram': predicted.value,
            'timestamp': datetime.now().isoformat(),
        })

        # 更新传统模型
        self.hexagram_model.record_sequence([current.value, predicted.value])

    def evaluate_sequence_quality(self, sequence: List[str]) -> float:
        """评估序列质量（向后兼容）"""
        if len(sequence) < 2:
            return 0.0

        quality = 0.5

        # 使用 sequence_patterns 评估
        pattern_key = ''.join(sequence[-3:]) if len(sequence) >= 3 else ''
        if pattern_key in self.hexagram_model.sequence_patterns:
            frequency = self.hexagram_model.sequence_patterns[pattern_key]
            quality += min(0.3, frequency * 0.05)

        try:
            for i in range(len(sequence) - 1):
                from_hex = HexagramType(sequence[i])
                to_hex = HexagramType(sequence[i + 1])
                prob = self.hexagram_model.transition_matrix.get(from_hex, {}).get(to_hex, 0)
                quality += prob * 0.1
        except ValueError:
            pass

        return min(1.0, max(0.0, quality))

    def suggest_intervention(
        self,
        current: HexagramType,
        target: HexagramType,
        memories: List[MemoryNode]
    ) -> Dict[str, Any]:
        """建议干预措施（向后兼容）"""
        predictions = self.hexagram_model.predict_next(current)

        if not predictions:
            return {'action': '等待观察', 'reason': '预测不确定'}

        current_pred = predictions[0][0]

        if current_pred == target:
            return {
                'action': '顺其自然',
                'reason': '当前发展趋势与目标一致',
                'confidence': predictions[0][1]
            }

        alternative_path = self._find_alternative_path(current, target)

        return {
            'action': '引导调整',
            'reason': f'当前趋势为{current_pred.value}，需要引导至{target.value}',
            'suggested_path': alternative_path,
            'confidence': predictions[0][1]
        }

    def _find_alternative_path(
        self,
        start: HexagramType,
        end: HexagramType
    ) -> List[str]:
        """寻找替代路径"""
        path = [start.value]
        current = start
        max_steps = 5

        for _ in range(max_steps):
            predictions = self.hexagram_model.predict_next(current)

            for hexagram, prob in predictions:
                if hexagram == end:
                    path.append(end.value)
                    return path

            if predictions:
                current = predictions[0][0]
                path.append(current.value)
            else:
                break

        return path
