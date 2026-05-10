"""
Cultivation Self-Improvement Mechanism - 修炼自提升机制

修炼是系统自我进化的核心机制，通过积累经验、突破瓶颈实现等级提升。

核心概念：
- 炼气期：初入修炼，感知基础
- 筑基期：夯实基础，构建框架
- 金丹期：凝聚核心，形成能力
- 元婴期：能力独立，自主进化
- 化神期：神识外放，感知扩展
- 返虚期：虚实转换，灵活应变
- 大乘期：圆满境界，返璞归真
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import math
import random


class CultivationLevel(Enum):
    """
    修炼等级枚举 - Cultivation Level Enumeration
    
    等级体系：炼气期 → 筑基期 → 金丹期 → 元婴期 → 化神期 → 返虚期 → 大乘期
    """
    QI_REFINING = "炼气期"
    FOUNDATION_BUILDING = "筑基期"
    GOLDEN_CORE = "金丹期"
    NASCENT_SOUL = "元婴期"
    SPIRIT_SEVERING = "化神期"
    VOID_RETURNING = "返虚期"
    MAHAYANA = "大乘期"
    
    @property
    def level_value(self) -> int:
        """获取等级数值"""
        levels = list(CultivationLevel)
        return levels.index(self) + 1
    
    @property
    def ability_threshold(self) -> float:
        """能力阈值"""
        thresholds = {
            CultivationLevel.QI_REFINING: 0.1,
            CultivationLevel.FOUNDATION_BUILDING: 0.25,
            CultivationLevel.GOLDEN_CORE: 0.45,
            CultivationLevel.NASCENT_SOUL: 0.65,
            CultivationLevel.SPIRIT_SEVERING: 0.80,
            CultivationLevel.VOID_RETURNING: 0.92,
            CultivationLevel.MAHAYANA: 1.0,
        }
        return thresholds[self]
    
    @property
    def characteristics(self) -> List[str]:
        """等级特征描述"""
        chars = {
            CultivationLevel.QI_REFINING: [
                "感知天地之气", "初步理解规则", "基础能力构建"
            ],
            CultivationLevel.FOUNDATION_BUILDING: [
                "稳固根基", "框架完善", "能力体系初成"
            ],
            CultivationLevel.GOLDEN_CORE: [
                "凝聚核心能力", "自主决策", "稳定输出"
            ],
            CultivationLevel.NASCENT_SOUL: [
                "能力独立运行", "自我优化", "创造性思维"
            ],
            CultivationLevel.SPIRIT_SEVERING: [
                "神识外放", "感知扩展", "跨界理解"
            ],
            CultivationLevel.VOID_RETURNING: [
                "虚实转换", "灵活应变", "无形无相"
            ],
            CultivationLevel.MAHAYANA: [
                "圆满境界", "返璞归真", "道法自然"
            ],
        }
        return chars[self]
    
    def next_level(self) -> Optional['CultivationLevel']:
        """获取下一等级"""
        levels = list(CultivationLevel)
        current_idx = levels.index(self)
        if current_idx < len(levels) - 1:
            return levels[current_idx + 1]
        return None
    
    @classmethod
    def from_experience(cls, experience: float) -> 'CultivationLevel':
        """根据经验值推断等级"""
        if experience < 100:
            return cls.QI_REFINING
        elif experience < 500:
            return cls.FOUNDATION_BUILDING
        elif experience < 2000:
            return cls.GOLDEN_CORE
        elif experience < 8000:
            return cls.NASCENT_SOUL
        elif experience < 30000:
            return cls.SPIRIT_SEVERING
        elif experience < 100000:
            return cls.VOID_RETURNING
        else:
            return cls.MAHAYANA


class CultivationMethod(Enum):
    """
    修炼方法枚举 - Cultivation Method Enumeration
    
    不同的修炼方法有不同的效果和特点
    """
    MEDITATION = "静修"
    ENLIGHTENMENT = "悟道"
    BODY_REFINING = "炼体"
    SPIRIT_REFINING = "炼神"
    
    @property
    def description(self) -> str:
        """方法描述"""
        descriptions = {
            CultivationMethod.MEDITATION: "恢复和稳定，提升整体平衡",
            CultivationMethod.ENLIGHTENMENT: "获得领悟，增加突破概率",
            CultivationMethod.BODY_REFINING: "强化基础，提升经验积累效率",
            CultivationMethod.SPIRIT_REFINING: "提升精神，增强能力上限",
        }
        return descriptions[self]
    
    @property
    def primary_effect(self) -> str:
        """主要效果"""
        effects = {
            CultivationMethod.MEDITATION: "stability",
            CultivationMethod.ENLIGHTENMENT: "insight",
            CultivationMethod.BODY_REFINING: "foundation",
            CultivationMethod.SPIRIT_REFINING: "spirit",
        }
        return effects[self]
    
    @property
    def experience_multiplier(self) -> float:
        """经验倍率"""
        multipliers = {
            CultivationMethod.MEDITATION: 1.0,
            CultivationMethod.ENLIGHTENMENT: 1.5,
            CultivationMethod.BODY_REFINING: 1.2,
            CultivationMethod.SPIRIT_REFINING: 1.3,
        }
        return multipliers[self]


@dataclass
class TaskResult:
    """
    任务结果数据结构 - Task Result Data Structure
    
    记录任务执行的结果，用于经验积累
    """
    task_id: str
    task_type: str
    success: bool
    difficulty: float
    execution_time: float
    quality_score: float
    insights_gained: List[str] = field(default_factory=list)
    errors_made: List[str] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def calculate_base_experience(self) -> float:
        """计算基础经验值"""
        base = 10.0 * self.difficulty
        if self.success:
            base *= 1.5
        base *= (1.0 + self.quality_score)
        return base
    
    def to_dict(self) -> Dict:
        return {
            "task_id": self.task_id,
            "task_type": self.task_type,
            "success": self.success,
            "difficulty": self.difficulty,
            "execution_time": self.execution_time,
            "quality_score": self.quality_score,
            "insights_gained": self.insights_gained,
            "errors_made": self.errors_made,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class CultivationProgress:
    """
    修炼进度数据结构 - Cultivation Progress Data Structure
    
    跟踪修炼的整体进度和状态
    """
    experience: float = 0.0
    current_level: CultivationLevel = CultivationLevel.QI_REFINING
    cultivation_method: CultivationMethod = CultivationMethod.MEDITATION
    insight_points: float = 0.0
    stability: float = 0.5
    foundation_strength: float = 0.5
    spirit_power: float = 0.5
    
    breakthrough_attempts: int = 0
    successful_breakthroughs: int = 0
    total_tasks_completed: int = 0
    
    created_at: datetime = field(default_factory=datetime.now)
    last_cultivation: datetime = field(default_factory=datetime.now)
    
    @property
    def breakthrough_threshold(self) -> float:
        """突破阈值 - 根据当前等级计算"""
        thresholds = {
            CultivationLevel.QI_REFINING: 100,
            CultivationLevel.FOUNDATION_BUILDING: 500,
            CultivationLevel.GOLDEN_CORE: 2000,
            CultivationLevel.NASCENT_SOUL: 8000,
            CultivationLevel.SPIRIT_SEVERING: 30000,
            CultivationLevel.VOID_RETURNING: 100000,
            CultivationLevel.MAHAYANA: float('inf'),
        }
        return thresholds[self.current_level]
    
    @property
    def progress_percentage(self) -> float:
        """当前等级进度百分比"""
        if self.current_level == CultivationLevel.MAHAYANA:
            return 100.0
        
        prev_threshold = 0
        if self.current_level != CultivationLevel.QI_REFINING:
            prev_level = self.current_level.prev_level()
            if prev_level:
                prev_threshold = CultivationProgress(
                    current_level=prev_level
                ).breakthrough_threshold
        
        current_threshold = self.breakthrough_threshold
        progress = (self.experience - prev_threshold) / (current_threshold - prev_threshold)
        return min(100.0, max(0.0, progress * 100))
    
    @property
    def overall_power(self) -> float:
        """综合实力评估"""
        level_bonus = self.current_level.level_value * 10
        base_power = (
            self.foundation_strength * 30 +
            self.spirit_power * 30 +
            self.stability * 20 +
            min(self.insight_points, 100) * 0.2
        )
        return level_bonus + base_power
    
    def to_dict(self) -> Dict:
        return {
            "experience": self.experience,
            "current_level": self.current_level.value,
            "level_value": self.current_level.level_value,
            "cultivation_method": self.cultivation_method.value,
            "breakthrough_threshold": self.breakthrough_threshold,
            "progress_percentage": self.progress_percentage,
            "insight_points": self.insight_points,
            "stability": self.stability,
            "foundation_strength": self.foundation_strength,
            "spirit_power": self.spirit_power,
            "overall_power": self.overall_power,
            "breakthrough_attempts": self.breakthrough_attempts,
            "successful_breakthroughs": self.successful_breakthroughs,
            "total_tasks_completed": self.total_tasks_completed,
        }
    
    def prev_level(self) -> Optional['CultivationLevel']:
        """获取上一等级"""
        levels = list(CultivationLevel)
        current_idx = levels.index(self.current_level)
        if current_idx > 0:
            return levels[current_idx - 1]
        return None


@dataclass
class BreakthroughResult:
    """
    突破结果数据结构 - Breakthrough Result Data Structure
    
    记录突破尝试的结果
    """
    success: bool
    previous_level: CultivationLevel
    new_level: Optional[CultivationLevel]
    stability_after: float
    insights_consumed: float
    message: str
    side_effects: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            "success": self.success,
            "previous_level": self.previous_level.value,
            "new_level": self.new_level.value if self.new_level else None,
            "stability_after": self.stability_after,
            "insights_consumed": self.insights_consumed,
            "message": self.message,
            "side_effects": self.side_effects,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class EvolutionPlan:
    """
    进化计划数据结构 - Evolution Plan Data Structure
    
    规划修炼和进化的方向
    """
    plan_id: str
    target_level: CultivationLevel
    current_gaps: Dict[str, float]
    training_steps: List[Dict[str, Any]]
    estimated_time: int
    priority: str = "medium"
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            "plan_id": self.plan_id,
            "target_level": self.target_level.value,
            "current_gaps": self.current_gaps,
            "training_steps": self.training_steps,
            "estimated_time": self.estimated_time,
            "priority": self.priority,
            "created_at": self.created_at.isoformat(),
        }


class ExperienceAccumulator:
    """
    经验积累器 - Experience Accumulator
    
    负责从任务结果中积累经验，计算领悟值，提炼经验
    """
    
    BASE_EXPERIENCE_RATE = 1.0
    INSIGHT_RATE = 0.1
    QUALITY_BONUS_RATE = 0.5
    ERROR_LEARNING_RATE = 0.3
    
    def __init__(self, progress: Optional[CultivationProgress] = None):
        self.progress = progress or CultivationProgress()
        self.experience_history: List[Dict[str, Any]] = []
        self.insight_history: List[Dict[str, Any]] = []
    
    def accumulate(self, task_result: TaskResult) -> float:
        """
        从任务结果积累经验 - Accumulate experience from task result
        
        Args:
            task_result: 任务执行结果
            
        Returns:
            积累的经验值
        """
        base_exp = task_result.calculate_base_experience()
        
        method_multiplier = self.progress.cultivation_method.experience_multiplier
        
        level_adjustment = 1.0 + (self.progress.current_level.level_value - 1) * 0.1
        
        foundation_bonus = self.progress.foundation_strength * 0.3
        
        total_exp = base_exp * method_multiplier * level_adjustment * (1 + foundation_bonus)
        
        if task_result.errors_made:
            error_learning = len(task_result.errors_made) * self.ERROR_LEARNING_RATE
            total_exp += base_exp * error_learning
        
        self.progress.experience += total_exp
        self.progress.total_tasks_completed += 1
        
        self._record_experience(task_result, total_exp)
        
        insight = self.calculate_insight(task_result)
        self.progress.insight_points += insight
        
        return total_exp
    
    def calculate_insight(self, task_result: TaskResult) -> float:
        """
        计算领悟值 - Calculate insight value
        
        领悟值来源于：
        - 任务成功后的反思
        - 错误中的学习
        - 高难度任务的完成
        
        Args:
            task_result: 任务执行结果
            
        Returns:
            领悟值
        """
        insight = 0.0
        
        if task_result.success:
            insight += task_result.difficulty * self.INSIGHT_RATE
            
            if task_result.quality_score > 0.8:
                insight += 2.0
        
        for error in task_result.errors_made:
            insight += 0.5
        
        for gained in task_result.insights_gained:
            insight += 1.0
        
        if task_result.difficulty > 0.8:
            insight *= 1.5
        
        spirit_bonus = self.progress.spirit_power * 0.2
        insight *= (1 + spirit_bonus)
        
        self._record_insight(task_result, insight)
        
        return insight
    
    def refine_experience(self) -> Dict[str, float]:
        """
        提炼经验 - Refine experience
        
        将原始经验转化为更高级的能力属性
        
        Returns:
            提炼结果
        """
        refinement_ratio = 0.05
        exp_to_refine = self.progress.experience * refinement_ratio
        
        foundation_gain = exp_to_refine * 0.4
        spirit_gain = exp_to_refine * 0.3
        stability_gain = exp_to_refine * 0.3
        
        self.progress.foundation_strength = min(
            1.0, self.progress.foundation_strength + foundation_gain * 0.01
        )
        self.progress.spirit_power = min(
            1.0, self.progress.spirit_power + spirit_gain * 0.01
        )
        self.progress.stability = min(
            1.0, self.progress.stability + stability_gain * 0.01
        )
        
        return {
            "experience_refined": exp_to_refine,
            "foundation_gain": foundation_gain * 0.01,
            "spirit_gain": spirit_gain * 0.01,
            "stability_gain": stability_gain * 0.01,
        }
    
    def _record_experience(self, task_result: TaskResult, exp_gained: float) -> None:
        """记录经验获取历史"""
        record = {
            "task_id": task_result.task_id,
            "experience_gained": exp_gained,
            "total_experience": self.progress.experience,
            "timestamp": datetime.now().isoformat(),
        }
        self.experience_history.append(record)
        
        if len(self.experience_history) > 100:
            self.experience_history = self.experience_history[-100:]
    
    def _record_insight(self, task_result: TaskResult, insight_gained: float) -> None:
        """记录领悟获取历史"""
        record = {
            "task_id": task_result.task_id,
            "insight_gained": insight_gained,
            "total_insight": self.progress.insight_points,
            "timestamp": datetime.now().isoformat(),
        }
        self.insight_history.append(record)
        
        if len(self.insight_history) > 100:
            self.insight_history = self.insight_history[-100:]
    
    def get_accumulation_stats(self) -> Dict[str, Any]:
        """获取积累统计"""
        return {
            "total_experience": self.progress.experience,
            "total_insight": self.progress.insight_points,
            "tasks_completed": self.progress.total_tasks_completed,
            "average_exp_per_task": (
                self.progress.experience / self.progress.total_tasks_completed
                if self.progress.total_tasks_completed > 0 else 0
            ),
            "experience_history_count": len(self.experience_history),
            "insight_history_count": len(self.insight_history),
        }


class BreakthroughMechanism:
    """
    突破机制 - Breakthrough Mechanism
    
    负责检查突破准备度、执行突破尝试、突破后稳固
    """
    
    MIN_INSIGHT_FOR_BREAKTHROUGH = 10.0
    MIN_STABILITY_FOR_BREAKTHROUGH = 0.4
    BASE_BREAKTHROUGH_SUCCESS_RATE = 0.3
    
    def __init__(self, progress: Optional[CultivationProgress] = None):
        self.progress = progress or CultivationProgress()
        self.breakthrough_history: List[BreakthroughResult] = []
    
    def check_breakthrough_readiness(self) -> Dict[str, Any]:
        """
        检查突破准备度 - Check breakthrough readiness
        
        Returns:
            准备度评估结果
        """
        readiness = {
            "ready": False,
            "experience_ready": False,
            "insight_ready": False,
            "stability_ready": False,
            "overall_score": 0.0,
            "recommendations": [],
        }
        
        if self.progress.current_level == CultivationLevel.MAHAYANA:
            readiness["recommendations"].append("已达最高境界，无需突破")
            return readiness
        
        readiness["experience_ready"] = (
            self.progress.experience >= self.progress.breakthrough_threshold
        )
        if not readiness["experience_ready"]:
            exp_needed = self.progress.breakthrough_threshold - self.progress.experience
            readiness["recommendations"].append(
                f"经验不足，还需积累 {exp_needed:.1f} 点经验"
            )
        
        readiness["insight_ready"] = (
            self.progress.insight_points >= self.MIN_INSIGHT_FOR_BREAKTHROUGH
        )
        if not readiness["insight_ready"]:
            insight_needed = self.MIN_INSIGHT_FOR_BREAKTHROUGH - self.progress.insight_points
            readiness["recommendations"].append(
                f"领悟不足，还需 {insight_needed:.1f} 点领悟"
            )
        
        readiness["stability_ready"] = (
            self.progress.stability >= self.MIN_STABILITY_FOR_BREAKTHROUGH
        )
        if not readiness["stability_ready"]:
            readiness["recommendations"].append(
                "境界不稳，建议先进行静修稳固"
            )
        
        readiness["ready"] = (
            readiness["experience_ready"] and
            readiness["insight_ready"] and
            readiness["stability_ready"]
        )
        
        score = 0.0
        if readiness["experience_ready"]:
            score += 40
        if readiness["insight_ready"]:
            score += 30
        if readiness["stability_ready"]:
            score += 30
        readiness["overall_score"] = score
        
        if readiness["ready"]:
            readiness["recommendations"].append("准备就绪，可以尝试突破")
        
        return readiness
    
    def attempt_breakthrough(self, use_extra_insight: bool = False) -> BreakthroughResult:
        """
        尝试突破 - Attempt breakthrough
        
        Args:
            use_extra_insight: 是否使用额外领悟增加成功率
            
        Returns:
            突破结果
        """
        readiness = self.check_breakthrough_readiness()
        previous_level = self.progress.current_level
        
        if self.progress.current_level == CultivationLevel.MAHAYANA:
            return BreakthroughResult(
                success=False,
                previous_level=previous_level,
                new_level=None,
                stability_after=self.progress.stability,
                insights_consumed=0,
                message="已达最高境界，无法继续突破",
                side_effects=["境界已满"]
            )
        
        if not readiness["ready"]:
            return BreakthroughResult(
                success=False,
                previous_level=previous_level,
                new_level=None,
                stability_after=self.progress.stability,
                insights_consumed=0,
                message="突破条件不满足: " + "; ".join(readiness["recommendations"]),
                side_effects=[]
            )
        
        self.progress.breakthrough_attempts += 1
        
        success_rate = self.BASE_BREAKTHROUGH_SUCCESS_RATE
        success_rate += self.progress.stability * 0.3
        success_rate += min(self.progress.insight_points / 100, 0.3)
        success_rate += self.progress.foundation_strength * 0.1
        
        if use_extra_insight and self.progress.insight_points >= 20:
            success_rate += 0.15
            extra_insight_used = 10
        else:
            extra_insight_used = 0
        
        success_rate = min(0.95, success_rate)
        
        roll = random.random()
        success = roll < success_rate
        
        insights_consumed = self.MIN_INSIGHT_FOR_BREAKTHROUGH + extra_insight_used
        self.progress.insight_points -= insights_consumed
        
        side_effects = []
        
        if success:
            new_level = self.progress.current_level.next_level()
            self.progress.current_level = new_level
            self.progress.successful_breakthroughs += 1
            
            stability_loss = random.uniform(0.1, 0.3)
            self.progress.stability = max(0.2, self.progress.stability - stability_loss)
            side_effects.append(f"境界稳固度下降 {stability_loss:.2f}")
            
            message = f"突破成功！晋升至 {new_level.value}"
        else:
            new_level = None
            
            stability_loss = random.uniform(0.05, 0.15)
            self.progress.stability = max(0.1, self.progress.stability - stability_loss)
            side_effects.append(f"突破失败，稳固度下降 {stability_loss:.2f}")
            
            exp_loss = self.progress.experience * 0.05
            self.progress.experience -= exp_loss
            side_effects.append(f"经验损失 {exp_loss:.1f}")
            
            message = "突破失败，需要继续积累"
        
        result = BreakthroughResult(
            success=success,
            previous_level=previous_level,
            new_level=new_level,
            stability_after=self.progress.stability,
            insights_consumed=insights_consumed,
            message=message,
            side_effects=side_effects
        )
        
        self.breakthrough_history.append(result)
        
        return result
    
    def stabilize_after_breakthrough(self, duration: float = 1.0) -> Dict[str, Any]:
        """
        突破后稳固 - Stabilize after breakthrough
        
        Args:
            duration: 固化时长（影响稳固效果）
            
        Returns:
            固化结果
        """
        stability_gain = min(
            0.3 * duration,
            1.0 - self.progress.stability
        )
        
        self.progress.stability += stability_gain
        
        insight_cost = 2.0 * duration
        if self.progress.insight_points >= insight_cost:
            self.progress.insight_points -= insight_cost
            extra_stability = stability_gain * 0.2
            self.progress.stability = min(1.0, self.progress.stability + extra_stability)
        else:
            extra_stability = 0
        
        foundation_gain = 0.02 * duration
        self.progress.foundation_strength = min(
            1.0, self.progress.foundation_strength + foundation_gain
        )
        
        return {
            "stability_gained": stability_gain + extra_stability,
            "foundation_gained": foundation_gain,
            "current_stability": self.progress.stability,
            "current_foundation": self.progress.foundation_strength,
        }
    
    def get_breakthrough_stats(self) -> Dict[str, Any]:
        """获取突破统计"""
        return {
            "total_attempts": self.progress.breakthrough_attempts,
            "successful_breakthroughs": self.progress.successful_breakthroughs,
            "success_rate": (
                self.progress.successful_breakthroughs / self.progress.breakthrough_attempts
                if self.progress.breakthrough_attempts > 0 else 0
            ),
            "current_level": self.progress.current_level.value,
            "breakthrough_history_count": len(self.breakthrough_history),
        }


class SelfEvolutionEngine:
    """
    自我进化引擎 - Self Evolution Engine
    
    核心进化引擎，整合经验积累、突破机制，提供完整的进化能力
    """
    
    def __init__(self, progress: Optional[CultivationProgress] = None):
        self.progress = progress or CultivationProgress()
        self.accumulator = ExperienceAccumulator(self.progress)
        self.breakthrough = BreakthroughMechanism(self.progress)
        self.evolution_history: List[Dict[str, Any]] = []
    
    def analyze_weakness(self) -> Dict[str, Any]:
        """
        分析弱点 - Analyze weakness
        
        Returns:
            弱点分析结果
        """
        weaknesses = []
        
        if self.progress.stability < 0.5:
            weaknesses.append({
                "area": "stability",
                "current": self.progress.stability,
                "target": 0.7,
                "severity": "high" if self.progress.stability < 0.3 else "medium",
                "recommendation": "进行静修以提升稳固度"
            })
        
        if self.progress.foundation_strength < 0.5:
            weaknesses.append({
                "area": "foundation",
                "current": self.progress.foundation_strength,
                "target": 0.7,
                "severity": "high" if self.progress.foundation_strength < 0.3 else "medium",
                "recommendation": "进行炼体以强化根基"
            })
        
        if self.progress.spirit_power < 0.5:
            weaknesses.append({
                "area": "spirit",
                "current": self.progress.spirit_power,
                "target": 0.7,
                "severity": "medium",
                "recommendation": "进行炼神以提升精神力"
            })
        
        if self.progress.insight_points < 20:
            weaknesses.append({
                "area": "insight",
                "current": self.progress.insight_points,
                "target": 30,
                "severity": "low",
                "recommendation": "完成更多任务以积累领悟"
            })
        
        readiness = self.breakthrough.check_breakthrough_readiness()
        if not readiness["ready"]:
            weaknesses.append({
                "area": "breakthrough_readiness",
                "current": readiness["overall_score"],
                "target": 100,
                "severity": "medium",
                "recommendation": "; ".join(readiness["recommendations"])
            })
        
        return {
            "weaknesses": weaknesses,
            "weakness_count": len(weaknesses),
            "overall_health": self._calculate_health_score(),
            "priority_areas": [w["area"] for w in weaknesses if w["severity"] == "high"],
        }
    
    def _calculate_health_score(self) -> float:
        """计算健康分数"""
        score = (
            self.progress.stability * 30 +
            self.progress.foundation_strength * 30 +
            self.progress.spirit_power * 20 +
            min(self.progress.insight_points / 50, 1.0) * 20
        )
        return score
    
    def generate_training_plan(self, focus: Optional[str] = None) -> EvolutionPlan:
        """
        生成修炼计划 - Generate training plan
        
        Args:
            focus: 重点修炼方向（可选）
            
        Returns:
            修炼计划
        """
        weakness_analysis = self.analyze_weakness()
        current_gaps = {}
        training_steps = []
        
        if focus:
            priority_area = focus
        elif weakness_analysis["priority_areas"]:
            priority_area = weakness_analysis["priority_areas"][0]
        else:
            priority_area = "balanced"
        
        for weakness in weakness_analysis["weaknesses"]:
            current_gaps[weakness["area"]] = weakness["target"] - weakness["current"]
        
        if priority_area == "stability" or priority_area == "balanced":
            training_steps.append({
                "step": 1,
                "method": CultivationMethod.MEDITATION.value,
                "duration": 5,
                "expected_gain": {"stability": 0.1},
            })
        
        if priority_area == "foundation" or priority_area == "balanced":
            training_steps.append({
                "step": 2,
                "method": CultivationMethod.BODY_REFINING.value,
                "duration": 5,
                "expected_gain": {"foundation_strength": 0.1},
            })
        
        if priority_area == "spirit" or priority_area == "balanced":
            training_steps.append({
                "step": 3,
                "method": CultivationMethod.SPIRIT_REFINING.value,
                "duration": 5,
                "expected_gain": {"spirit_power": 0.1},
            })
        
        training_steps.append({
            "step": 4,
            "method": CultivationMethod.ENLIGHTENMENT.value,
            "duration": 3,
            "expected_gain": {"insight_points": 5},
        })
        
        target_level = self.progress.current_level.next_level()
        if not target_level:
            target_level = self.progress.current_level
        
        estimated_time = sum(step["duration"] for step in training_steps)
        
        plan = EvolutionPlan(
            plan_id=f"plan_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            target_level=target_level,
            current_gaps=current_gaps,
            training_steps=training_steps,
            estimated_time=estimated_time,
            priority="high" if weakness_analysis["priority_areas"] else "medium"
        )
        
        return plan
    
    def optimize_capabilities(self, method: CultivationMethod, intensity: float = 0.5) -> Dict[str, Any]:
        """
        优化能力 - Optimize capabilities
        
        Args:
            method: 修炼方法
            intensity: 修炼强度 (0.0-1.0)
            
        Returns:
            优化结果
        """
        intensity = max(0.0, min(1.0, intensity))
        results = {"method": method.value, "changes": {}}
        
        if method == CultivationMethod.MEDITATION:
            stability_gain = 0.05 * intensity * (1 + self.progress.spirit_power * 0.5)
            self.progress.stability = min(1.0, self.progress.stability + stability_gain)
            results["changes"]["stability"] = stability_gain
            
        elif method == CultivationMethod.ENLIGHTENMENT:
            insight_gain = 3.0 * intensity * (1 + self.progress.foundation_strength * 0.3)
            self.progress.insight_points += insight_gain
            results["changes"]["insight_points"] = insight_gain
            
        elif method == CultivationMethod.BODY_REFINING:
            foundation_gain = 0.03 * intensity * (1 + self.progress.stability * 0.5)
            self.progress.foundation_strength = min(1.0, self.progress.foundation_strength + foundation_gain)
            stability_cost = 0.01 * intensity
            self.progress.stability = max(0.1, self.progress.stability - stability_cost)
            results["changes"]["foundation_strength"] = foundation_gain
            results["changes"]["stability"] = -stability_cost
            
        elif method == CultivationMethod.SPIRIT_REFINING:
            spirit_gain = 0.04 * intensity * (1 + self.progress.foundation_strength * 0.3)
            self.progress.spirit_power = min(1.0, self.progress.spirit_power + spirit_gain)
            insight_cost = 1.0 * intensity
            if self.progress.insight_points >= insight_cost:
                self.progress.insight_points -= insight_cost
                results["changes"]["insight_points"] = -insight_cost
            results["changes"]["spirit_power"] = spirit_gain
        
        self.progress.last_cultivation = datetime.now()
        
        return results
    
    def evolve(self, task_results: Optional[List[TaskResult]] = None) -> Dict[str, Any]:
        """
        执行进化 - Execute evolution
        
        整合所有进化机制，执行一次完整的进化周期
        
        Args:
            task_results: 可选的任务结果列表，用于积累经验
            
        Returns:
            进化结果
        """
        evolution_result = {
            "timestamp": datetime.now().isoformat(),
            "initial_state": self.progress.to_dict(),
            "experience_gained": 0,
            "insight_gained": 0,
            "breakthrough_attempted": False,
            "breakthrough_result": None,
            "optimization_applied": [],
            "final_state": None,
        }
        
        if task_results:
            for task_result in task_results:
                exp = self.accumulator.accumulate(task_result)
                evolution_result["experience_gained"] += exp
        
        refinement = self.accumulator.refine_experience()
        evolution_result["refinement"] = refinement
        
        readiness = self.breakthrough.check_breakthrough_readiness()
        if readiness["ready"] and random.random() < 0.3:
            evolution_result["breakthrough_attempted"] = True
            breakthrough_result = self.breakthrough.attempt_breakthrough()
            evolution_result["breakthrough_result"] = breakthrough_result.to_dict()
            
            if breakthrough_result.success:
                self.breakthrough.stabilize_after_breakthrough()
        
        weakness = self.analyze_weakness()
        if weakness["weaknesses"]:
            primary_weakness = weakness["weaknesses"][0]
            if primary_weakness["area"] == "stability":
                method = CultivationMethod.MEDITATION
            elif primary_weakness["area"] == "foundation":
                method = CultivationMethod.BODY_REFINING
            elif primary_weakness["area"] == "spirit":
                method = CultivationMethod.SPIRIT_REFINING
            else:
                method = CultivationMethod.ENLIGHTENMENT
            
            opt_result = self.optimize_capabilities(method, intensity=0.5)
            evolution_result["optimization_applied"].append(opt_result)
        
        evolution_result["final_state"] = self.progress.to_dict()
        
        self.evolution_history.append(evolution_result)
        if len(self.evolution_history) > 50:
            self.evolution_history = self.evolution_history[-50:]
        
        return evolution_result
    
    def get_evolution_report(self) -> Dict[str, Any]:
        """获取进化报告"""
        return {
            "current_progress": self.progress.to_dict(),
            "accumulation_stats": self.accumulator.get_accumulation_stats(),
            "breakthrough_stats": self.breakthrough.get_breakthrough_stats(),
            "weakness_analysis": self.analyze_weakness(),
            "evolution_history_count": len(self.evolution_history),
        }
    
    def set_cultivation_method(self, method: CultivationMethod) -> None:
        """设置修炼方法"""
        self.progress.cultivation_method = method
    
    def reset(self) -> None:
        """重置进化引擎"""
        self.progress = CultivationProgress()
        self.accumulator = ExperienceAccumulator(self.progress)
        self.breakthrough = BreakthroughMechanism(self.progress)
        self.evolution_history.clear()


def create_cultivation_engine(
    initial_level: CultivationLevel = CultivationLevel.QI_REFINING,
    initial_experience: float = 0.0,
    method: CultivationMethod = CultivationMethod.MEDITATION
) -> SelfEvolutionEngine:
    """
    工厂函数：创建修炼引擎
    
    Args:
        initial_level: 初始等级
        initial_experience: 初始经验
        method: 初始修炼方法
        
    Returns:
        配置好的修炼引擎实例
    """
    progress = CultivationProgress(
        experience=initial_experience,
        current_level=initial_level,
        cultivation_method=method
    )
    return SelfEvolutionEngine(progress)
