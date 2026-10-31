"""
Main Oriental Wisdom Agent - Core System Integration
东方智慧智能体主模块 - 核心系统集成
"""

import asyncio
import re
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, field

from config.settings import get_config
from core.types import (
    MemoryLayer, WuxingType, SenseType,
    ExecutionTask, ThinkingContext, TimeHorizon
)
# prediction_engine.HexagramType 才是完整六十四卦，core.types.HexagramType 只有八卦
from prediction.prediction_engine import PredictionEngine, HexagramType

from memory.system import MemorySystem
from thinking.system import ThinkingSystem
from execution.system import ExecutionSystem
from perception.system import PerceptionSystem
from body.system import BodyMappingSystem
from image.system import ImageAndQiSystem

from commercial.agent import CommercialAgent, ShangDaoAdvisor


# ============ 数据类 ============

@dataclass
class AgentState:
    """智能体状态"""
    status: str
    uptime: float
    cycle_count: int
    energy_level: float
    vitality: float
    active_systems: List[str]


@dataclass
class AgentResponse:
    """智能体响应"""
    response_text: str
    actions_taken: List[Dict[str, Any]]
    memory_updates: List[str]
    state_changes: Dict[str, Any]


# ============ 中文辅助工具 ============

# 中文关键词词典：用户常问主题 → 扩展关键词列表
_KEYWORD_DICT: Dict[str, List[str]] = {
    '商机': ['商机', '创业', '机会', '项目', '市场', '创业机会'],
    '投资': ['投资', '投', '融资', '回报', '回报', '收益', '风险'],
    '竞争': ['竞争', '对手', '对手', '对手', '竞争对手', '格局'],
    '商业模式': ['商业模式', '盈利', '变现', '收入', '成本'],
    '战略': ['战略', '策略', '布局', '长远', '方向'],
    '预测': ['预测', '卦', '卜', '算命', '易经', '梅花', '吉凶'],
    '身体': ['身体', '健康', '养生', '经络', '气血', '精神', '精气神'],
    '修炼': ['修炼', '修真', '功夫', '打坐', '冥想', '境界'],
    '情绪': ['情绪', '焦虑', '抑郁', '压力', '心', '心情'],
    '关系': ['关系', '人际', '合作', '矛盾', '沟通'],
    '金钱': ['金钱', '钱', '财务', '财运', '钱'],
    '运势': ['运势', '运气', '运程', '流年', '吉凶'],
    '五行': ['五行', '金木水火土', '生克'],
    '阴阳': ['阴阳', '太极', '平衡'],
    '八卦': ['八卦', '六十四卦', '乾坤震巽'],
}


def _extract_chinese_keywords(text: str, top_n: int = 8) -> List[str]:
    """
    中文关键词提取：字符 n-gram + 词典匹配，无需依赖 jieba。
    思路：2-gram/3-gram 作为基础，再用词典补全，去重取前 N。
    """
    text = text.strip()
    if not text:
        return []

    # 1. 英文/数字词直接 split
    english_words = re.findall(r'[a-zA-Z]{2,}', text)

    # 2. 中文字符 2/3/4-gram 提取
    chinese_chars = re.findall(r'[\u4e00-\u9fff]+', text)
    ngrams: List[str] = []
    for chunk in chinese_chars:
        for n in (2, 3, 4):
            for i in range(len(chunk) - n + 1):
                ngrams.append(chunk[i:i + n])

    # 3. 词典匹配
    dict_matches: List[str] = []
    for key, expansions in _KEYWORD_DICT.items():
        if any(k in text for k in [key] + expansions[:2]):
            dict_matches.append(key)

    # 4. 加权去重
    scored: Dict[str, int] = {}
    for g in ngrams:
        scored[g] = scored.get(g, 0) + 1
    for w in english_words:
        scored[w] = scored.get(w, 0) + 2
    for d in dict_matches:
        scored[d] = scored.get(d, 0) + 3  # 词典词权重最高

    # 过滤掉包含标点或过短的 gram
    items = sorted(scored.items(), key=lambda x: -x[1])
    result: List[str] = []
    seen = set()
    for kw, _ in items:
        if kw in seen:
            continue
        # 跳过完全被已收录词包含的 gram（如 "商业" 和 "商业模式" 同时出现时保留后者）
        if any(kw in r or r in kw for r in result):
            continue
        result.append(kw)
        seen.add(kw)
        if len(result) >= top_n:
            break

    return result


def _detect_intent(text: str) -> List[Tuple[str, float]]:
    """
    启发式意图识别，返回 [(intent, 置信度), ...] 按置信度降序。
    支持多意图场景（例如"我想创业投资"同时命中商机+投资）。
    """
    intents: List[Tuple[str, float]] = []
    t = text

    checks = [
        ('commercial_opportunity', 0.85, ['商机', '创业', '创业机会', '创业项目', '市场机会', '好项目', '开店', '做生意', '时机好', '能做吗', '赚钱', '能赚钱']),
        ('investment',            0.85, ['投资', '融资', '回报', '收益', '回报', '投什么', '入股', '风险大']),
        ('strategy',              0.80, ['战略', '策略', '布局', '方向', '怎么做大', '发展']),
        ('competition',           0.80, ['竞争', '对手', '格局', '打败', '脱颖而出', '价格战']),
        ('prediction',            0.75, ['预测', '卜', '卦', '易经', '吉凶', '会怎样', '会成功吗', '起卦', '占卜']),
        ('body_health',           0.70, ['身体', '健康', '养生', '经络', '气血', '精气神', '失眠', '精力']),
        ('cultivation',           0.70, ['修炼', '修真', '打坐', '冥想', '境界', '修行']),
        ('emotion_support',       0.65, ['焦虑', '压力', '心情不好', '抑郁', '痛苦', '难受', '崩溃', '不开心', '难受']),
        ('relationship',          0.65, ['关系', '合作', '人际', '矛盾', '怎么相处', '合伙']),
        ('wisdom_advice',         0.50, ['怎么办', '怎么看', '如何', '该不该', '应该', '建议']),
        ('introduce_self',        0.80, ['介绍', '你是谁', '你能做', '你是干什么']),
        ('hello',                 0.60, ['你好', 'hi', 'hello', '您好', '在吗', '小缘你好']),
    ]

    for intent, base_conf, keywords in checks:
        hit = sum(1 for k in keywords if k in t)
        if hit > 0:
            conf = min(1.0, base_conf + 0.05 * (hit - 1))
            intents.append((intent, conf))

    intents.sort(key=lambda x: -x[1])
    return intents


# ============ 主智能体 ============

class OrientalWisdomAgent:
    """东方智慧智能体主类 - 融合商道、预测、修炼、身体等子系统"""

    def __init__(self, config_path: Optional[str] = None):
        self.config = get_config(config_path)

        self.memory_system = MemorySystem(self.config)
        self.thinking_system = ThinkingSystem(self.config, self.memory_system)
        self.execution_system = ExecutionSystem(self.config)
        self.perception_system = PerceptionSystem(self.config)
        self.body_system = BodyMappingSystem(self.config)
        self.image_system = ImageAndQiSystem(self.config)

        # 商道智能系统
        self.commercial_agent = CommercialAgent()
        self.shangdao_advisor = ShangDaoAdvisor()

        # 预测引擎（主对话里直接调用）
        self._prediction_engine = PredictionEngine()

        self.status = "initialized"
        self.start_time: Optional[datetime] = None
        self.cycle_count = 0

        self._main_loop_task: Optional[asyncio.Task] = None
        self._is_running = False

    async def start(self) -> None:
        """启动智能体"""
        if self.status == "running":
            return

        self.start_time = datetime.now()
        self.status = "starting"

        await self.memory_system.start()
        await self.execution_system.start()

        self._is_running = True
        self._main_loop_task = asyncio.create_task(self._main_loop())

        self.status = "running"

    async def stop(self) -> None:
        """停止智能体"""
        self._is_running = False

        if self._main_loop_task:
            self._main_loop_task.cancel()
            try:
                await self._main_loop_task
            except asyncio.CancelledError:
                pass

        await self.memory_system.stop()
        await self.execution_system.stop()

        self.status = "stopped"

    # ============ 主对话处理 ============

    async def process(self, input_data: Any) -> AgentResponse:
        """处理输入 - 多意图路由 + 子系统真正参与"""
        self.cycle_count += 1

        response_text = ""
        actions_taken: List[Dict[str, Any]] = []
        memory_updates: List[str] = []
        state_changes: Dict[str, Any] = {}
        sub_responses: List[str] = []  # 各子系统输出片段

        if not isinstance(input_data, str):
            return AgentResponse(
                response_text="请用中文描述您的问题，我来帮您分析。",
                actions_taken=[],
                memory_updates=[],
                state_changes={}
            )

        text = input_data.strip()
        if not text:
            return AgentResponse(
                response_text="请告诉我您想了解什么，我可以从商道、预测、养生、修炼等角度为您分析。",
                actions_taken=[],
                memory_updates=[],
                state_changes={}
            )

        # 1. 意图识别
        detected_intents = _detect_intent(text)
        primary_intent = detected_intents[0][0] if detected_intents else 'wisdom_advice'

        # 2. 感知系统
        perception = self.perception_system.perceive(SenseType.MENTAL, {'thought': text})

        # 3. 中文关键词记忆检索
        query = self._create_memory_query(text)
        relevant_memories = await self.memory_system.retrieve(query)

        # 4. 根据意图调用对应子系统
        thinking_context = ThinkingContext(
            question=text,
            situation={'input': text, 'intent': primary_intent},
            available_options=self._generate_options(text),
            relevant_memories=relevant_memories
        )

        # 对每个高置信度意图执行对应动作
        for intent, conf in detected_intents:
            if conf < 0.6:
                continue
            result = self._dispatch_intent(intent, text)
            if result:
                sub_responses.append(result)
                actions_taken.append({'intent': intent, 'confidence': conf, 'action': intent})

        # 5. 三教融合思考（所有场景都做，保证哲学底色）
        thinking_result = await self.thinking_system.analyze(thinking_context)

        # 6. 存储记忆
        memory_id = await self.memory_system.store(
            content=text,
            memory_type=self._pick_memory_hexagram(primary_intent),
            layer=MemoryLayer.HUMAN,
            context={'cycle': self.cycle_count, 'intent': primary_intent}
        )
        memory_updates.append(memory_id)

        # 7. 身体状态更新
        body_health = await self.body_system.diagnose_health()
        await self.image_system.update_image_state({
            'vitality': body_health.vitality_score,
            'activity_level': 'thinking' if thinking_result.confidence > 0.6 else 'resting'
        })

        # 8. 整合最终响应
        response_text = self._generate_response(text, thinking_result, sub_responses, detected_intents)

        state_changes = {
            'cycle': self.cycle_count,
            'primary_intent': primary_intent,
            'detected_intents': detected_intents[:3],
            'vitality': body_health.vitality_score,
            'thinking_confidence': thinking_result.confidence,
            'philosophy_contributions': thinking_result.philosophy_contributions,
            'sub_systems_invoked': [a['intent'] for a in actions_taken],
        }

        return AgentResponse(
            response_text=response_text,
            actions_taken=actions_taken,
            memory_updates=memory_updates,
            state_changes=state_changes
        )

    def _create_memory_query(self, input_data: str):
        """创建记忆查询 - 中文关键词 n-gram + 词典扩展"""
        from core.types import MemoryQuery, QueryType
        keywords = _extract_chinese_keywords(input_data)
        if not keywords:
            keywords = input_data.split()[:3] or [input_data[:6]]
        return MemoryQuery(
            query_type=QueryType.KEYWORD,
            keywords=keywords,
            limit=10
        )

    def _generate_options(self, input_data: str) -> List[str]:
        """生成可选策略 - 基于意图的动态启发式"""
        intents = _detect_intent(input_data)
        primary = intents[0][0] if intents else 'wisdom_advice'

        option_map: Dict[str, List[str]] = {
            'commercial_opportunity': [
                '系统扫描市场机会并评估进入门槛',
                '分析商业模式盈利性与竞争格局',
                '结合商道智慧给出天时地利人和判断',
            ],
            'investment': [
                '使用 DCF/ROI 模型评估回报',
                '从五行生克视角判断风险时机',
                '综合评分并给出投资建议',
            ],
            'strategy': [
                '制定分阶段战略路线图',
                '分析竞争格局与差异化定位',
                '结合周易智慧给出战略时机建议',
            ],
            'competition': [
                '五力模型分析竞争强度',
                'SWOT 分析找出差异化优势',
                '结合商道给出竞争策略建议',
            ],
            'prediction': [
                '易经六十四卦推演吉凶',
                '干支时空能量计算应期',
                '综合多维度推理给出概率判断',
            ],
            'body_health': [
                '经络能量诊断与健康评估',
                '五行调理方案推荐',
                '结合精气神给出养生建议',
            ],
            'cultivation': [
                '评估当前修炼境界与瓶颈',
                '制定渐进式修炼路线图',
                '结合武道五禽戏给出锻炼方案',
            ],
            'emotion_support': [
                '情绪能量诊断（喜怒忧恐惊）',
                '道家无为建议化解内心焦虑',
                '儒家中庸之道平衡情绪',
            ],
            'relationship': [
                '人际五行关系分析（生克）',
                '儒家仁义礼智信建议',
                '给出沟通与相处策略',
            ],
        }

        if primary in option_map:
            return option_map[primary]

        # 通用：没有识别到明确意图
        return [
            '从易经角度推演变化趋势',
            '结合三教智慧给出综合建议',
            '调用预测系统评估概率',
            '记忆关联分析历史经验',
        ]

    def _pick_memory_hexagram(self, intent: str) -> HexagramType:
        """根据意图选记忆卦象"""
        mapping = {
            'commercial_opportunity': HexagramType.GUA_40,   # 益卦
            'investment':            HexagramType.GUA_57,   # 既济
            'strategy':              HexagramType.GUA_10,   # 泰卦
            'competition':           HexagramType.GUA_41,   # 夬卦（决断）
            'prediction':            HexagramType.QIAN,     # 乾卦
            'body_health':           HexagramType.GUA_50,   # 艮卦（止）
            'cultivation':           HexagramType.GUA_25,   # 颐卦
            'emotion_support':       HexagramType.GUA_51,   # 渐卦
            'relationship':          HexagramType.GUA_7,    # 小畜
            'introduce_self':        HexagramType.LI,
            'hello':                 HexagramType.LI,
        }
        return mapping.get(intent, HexagramType.GUA_11)  # 默认同人卦

    # ============ 意图分发 ============

    def _dispatch_intent(self, intent: str, text: str) -> Optional[str]:
        """根据意图调用子系统，返回该子系统的输出片段字符串"""
        try:
            if intent == 'commercial_opportunity':
                result = self.commercial_agent.analyze_opportunity({'query': text})
                if isinstance(result, dict):
                    opp_type = result.get('opportunity_type', '商机分析')
                    score = result.get('market_score', result.get('feasibility', 0))
                    return f"📊 商道洞察：{opp_type}，机会评分 {score:.2f}" if isinstance(score, (int, float)) else f"📊 商道洞察：{opp_type}"
                return None

            elif intent == 'investment':
                result = self.commercial_agent.analyze_investment({'query': text})
                if isinstance(result, dict):
                    ir = result.get('risk_return_index', result.get('roi', 0))
                    risk = result.get('risk_level', '')
                    rr = f"风险等级 {risk}" if risk else ""
                    return f"💰 投资分析：风险回报指数 {ir:.2f}，{rr}".strip() if isinstance(ir, (int, float)) else f"💰 投资分析：{rr}"
                return None

            elif intent == 'strategy':
                result = self.commercial_agent.formulate_strategy({'query': text})
                if isinstance(result, dict):
                    direction = result.get('strategic_direction', '战略方向')
                    return f"🎯 战略建议：{direction}"
                return None

            elif intent == 'competition':
                result = self.commercial_agent.analyze_competition({'query': text}, None)
                if isinstance(result, dict):
                    intensity = result.get('competition_intensity', '')
                    return f"⚔️ 竞争分析：{intensity}" if intensity else None
                return None

            elif intent == 'prediction':
                # 直接走 PredictionEngine（易经 + 梅花 + 五行 + 干支综合）
                pred = self._prediction_engine.predict(text)
                # 综合预测 result 是 ensemble dict，hexagram 在第一个子预测里
                hex_name = ''
                if isinstance(pred.result, dict):
                    sub_preds = pred.result.get('predictions', [])
                    if sub_preds and isinstance(sub_preds[0], dict):
                        hex_name = sub_preds[0].get('hexagram', '')
                conf = pred.confidence
                prob = pred.probability
                interp = pred.interpretation or ''
                return f"🔮 预测推演：{hex_name or '起卦推演'}，置信度 {conf:.2f}，综合概率 {prob:.2f}。{interp}"

            elif intent == 'introduce_self':
                return None  # 走 _generate_response 主路径

        except Exception as e:
            # 子系统异常不影响主对话，只记日志（上层统一处理）
            import logging
            logging.getLogger(__name__).warning(f"dispatch intent {intent} error: {e}")
            return None

        return None

    # ============ 响应生成 ============

    def _generate_response(
        self,
        original_input: str,
        thinking_result,
        sub_responses: List[str],
        intents: List[Tuple[str, float]]
    ) -> str:
        """融合多来源输出生成最终回答"""
        primary_intent = intents[0][0] if intents else 'wisdom_advice'

        # 特殊场景：自我介绍
        if primary_intent == 'introduce_self':
            return (
                "我是东方智慧智能体——融合中国哲学与现代 AI 的思考伙伴。\n"
                "我能做的事：\n"
                "  • 商道智能：商机洞察、商业模式评估、竞争分析、投资决策\n"
                "  • 智能预测：易经卦象推演、梅花易数、五行生克、干支时空综合判断\n"
                "  • 养生修炼：经络能量诊断、精气神调理、武道五禽戏指导\n"
                "  • 情绪与人际：结合儒家仁义礼智信与道家无为的建议\n"
                "  • 三教融合思考：佛家因果 + 道家辩证 + 儒家中庸\n\n"
                "您可以直接问我：'现在创业好不好？'、'帮我预测这个项目能成吗？'、"
                "'我最近身体状态怎么样？'，我会从多角度为您分析。"
            )

        if primary_intent == 'hello':
            return "您好！我是东方智慧智能体，很高兴为您服务。请问您想了解什么？"

        # 基础层：三教融合思考结论
        conclusion = thinking_result.conclusion or {}
        if not isinstance(conclusion, dict):
            conclusion = {}

        dialectical_insight = conclusion.get('dialectical_insight', '')
        harmony_with_tao = conclusion.get('harmony_with_tao', 0.5)
        confidence = thinking_result.confidence

        # 哲学贡献展开
        contributions = thinking_result.philosophy_contributions or {}
        top_philos = sorted(contributions.items(), key=lambda x: -x[1])[:2]
        philos_text = '、'.join(
            f"{name} {score:.2f}" for name, score in top_philos
        ) if top_philos else ''

        # 推荐动作
        recs = thinking_result.recommended_actions or []
        rec_text = ''
        if recs:
            top_recs = recs[:3]
            rec_text = '\n    建议行动：' + '；'.join(top_recs)

        # 组装回答
        parts: List[str] = []

        # 子系统输出先放前面（具体数据更直观）
        for sr in sub_responses:
            if sr:
                parts.append(sr)

        # 思考层结论
        insight_line = f"思考洞察：{dialectical_insight}" if dialectical_insight else None
        harmony_line = f"合道程度：{harmony_with_tao:.2f}"
        conf_line = f"整体置信度：{confidence:.2f}"

        philosophy_line = f"哲学底色：{philos_text}" if philos_text else None

        body = [p for p in [insight_line, harmony_line, conf_line, philosophy_line] if p]
        if body:
            parts.append('\n'.join(body))

        if rec_text:
            parts.append(rec_text)

        return '\n\n'.join(parts) if parts else (
            f"我已综合分析您的问题，置信度 {confidence:.2f}。"
            f"合道程度 {harmony_with_tao:.2f}，辩证洞察：{dialectical_insight or '变化之中自有定数'}。"
        )

    # ============ 主循环 & 状态 ============

    async def _main_loop(self) -> None:
        """主循环"""
        cycle_duration = self.config.get('core.system_cycle_duration', 0.5)

        while self._is_running:
            try:
                await asyncio.sleep(cycle_duration)

                if self.execution_system:
                    await self.execution_system.optimize_energy()

                body_state = await self.body_system.get_system_state()
                if body_state.get('vitality', 1.0) < 0.3:
                    await self.body_system.repair('full')

            except asyncio.CancelledError:
                break
            except Exception:
                pass

    async def get_state(self) -> AgentState:
        """获取状态"""
        uptime = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0

        memory_state = await self.memory_system.get_system_state()
        body_state = await self.body_system.get_system_state()
        image_state = await self.image_system.get_system_state()

        energy_level = body_state.get('metabolism', {}).get('qi_total', 0) / 100.0
        vitality = body_state.get('vitality', 0.8)

        return AgentState(
            status=self.status,
            uptime=uptime,
            cycle_count=self.cycle_count,
            energy_level=energy_level,
            vitality=vitality,
            active_systems=['memory', 'thinking', 'execution', 'perception', 'body', 'image', 'commercial', 'prediction']
        )

    async def get_full_state(self) -> Dict[str, Any]:
        """获取完整状态"""
        return {
            'agent': {
                'status': self.status,
                'uptime': (datetime.now() - self.start_time).total_seconds() if self.start_time else 0,
                'cycle_count': self.cycle_count
            },
            'memory': await self.memory_system.get_system_state(),
            'thinking': await self.thinking_system.get_system_state(),
            'execution': await self.execution_system.get_system_state(),
            'perception': self.perception_system.get_system_state(),
            'body': await self.body_system.get_system_state(),
            'image': await self.image_system.get_system_state(),
            'commercial': self.commercial_agent.get_state(),
            'prediction_history_len': len(self._prediction_engine.prediction_history),
        }

    # ==================== 商道智能系统接口 ====================

    def analyze_business_opportunity(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.commercial_agent.analyze_opportunity(market_data)

    def analyze_business_model(self, model_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.commercial_agent.analyze_business_model(model_data)

    def analyze_competition(
        self,
        competitor_data: Dict[str, Any],
        market_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        return self.commercial_agent.analyze_competition(competitor_data, market_data)

    def analyze_investment(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.commercial_agent.analyze_investment(project_data)

    def formulate_strategy(self, business_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.commercial_agent.formulate_strategy(business_data)

    def generate_commercial_report(self, context: Dict[str, Any]) -> Any:
        return self.commercial_agent.generate_comprehensive_report(context)

    def get_shangdao_wisdom(self) -> List[Dict[str, Any]]:
        return self.commercial_agent.get_wisdom_insights()

    def get_shangdao_advice(self, situation: str) -> Dict[str, str]:
        return self.shangdao_advisor.get_advice(situation)

    def evaluate_business_decision(
        self,
        decision: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        return self.shangdao_advisor.evaluate_decision(decision, context)


async def create_agent(config_path: Optional[str] = None) -> OrientalWisdomAgent:
    """创建智能体实例"""
    agent = OrientalWisdomAgent(config_path)
    await agent.start()
    return agent


if __name__ == "__main__":
    async def main():
        agent = await create_agent()

        print("东方智慧智能体已启动")
        print("=" * 50)

        # 测试几个典型对话
        for q in [
            "你是谁，能做什么？",
            "现在创业有什么好机会吗？",
            "帮我预测一下这个项目能成吗？",
        ]:
            resp = await agent.process(q)
            print(f"\nQ: {q}")
            print(f"A: {resp.response_text}")

        state = await agent.get_state()
        print(f"\n智能体状态: 运行 {state.uptime:.2f}s, 循环 {state.cycle_count}, 活力 {state.vitality:.2f}")

        await agent.stop()
        print("\n智能体已停止")

    asyncio.run(main())
