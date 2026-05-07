"""
统一模型路由网关
================
将多个 AI 服务商（小米MiMo、OpenRouter、阿里云百炼、DeepSeek、智谱GLM）
整合为统一的 OpenAI 兼容 API 接口，支持智能路由、熔断保护、限速检测、自动更新。

对外暴露: POST /v1/chat/completions (OpenAI 兼容格式)
"""

import asyncio
import json
import logging
import os
import re
import time
import hashlib
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
import uvicorn

# ============================================================
# 日志配置
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("model-router")

# ============================================================
# 配置加载
# ============================================================
CONFIG_PATH = os.environ.get("ROUTER_CONFIG_PATH", "config.json")


def load_config(path: str) -> dict:
    """加载配置文件，支持环境变量替换"""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    # 替换 ${ENV_VAR} 为环境变量值
    def replace_env(match):
        var_name = match.group(1)
        return os.environ.get(var_name, match.group(0))
    content = re.sub(r'\$\{(\w+)\}', replace_env, content)
    config = json.loads(content)
    logger.info(f"配置加载成功，版本 v{config.get('version', '?')}")
    return config


# ============================================================
# 熔断器 (Circuit Breaker)
# ============================================================
class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass
class CircuitBreaker:
    """熔断器：保护模型调用，防止故障扩散"""
    name: str
    failure_threshold: int = 3
    recovery_timeout: float = 60.0
    half_open_max_probes: int = 1
    slow_threshold: float = 25.0

    state: CircuitState = field(default=CircuitState.CLOSED, init=False)
    failure_count: int = field(default=0, init=False)
    success_count: int = field(default=0, init=False)
    last_failure_time: float = field(default=0.0, init=False)
    half_open_calls: int = field(default=0, init=False)
    total_requests: int = field(default=0, init=False)
    error_requests: int = field(default=0, init=False)
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock, init=False)

    def can_execute(self) -> bool:
        self.total_requests += 1
        if self.state == CircuitState.CLOSED:
            return True
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time >= self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                self.half_open_calls = 0
                logger.info(f"[熔断器] {self.name} 进入半开状态，开始试探")
                return True
            return False
        # HALF_OPEN
        if self.half_open_calls < self.half_open_max_probes:
            self.half_open_calls += 1
            return True
        return False

    def record_success(self, response_time: float = 0):
        self.success_count += 1
        if self.state == CircuitState.HALF_OPEN:
            logger.info(f"[熔断器] {self.name} 试探成功，恢复正常")
            self._reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0

    def record_failure(self, error_type: str = "", response_time: float = 0):
        self.error_requests += 1
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.state == CircuitState.HALF_OPEN:
            logger.warning(f"[熔断器] {self.name} 试探失败，重新熔断 (错误: {error_type})")
            self.state = CircuitState.OPEN
        elif self.failure_count >= self.failure_threshold:
            logger.warning(
                f"[熔断器] {self.name} 连续失败 {self.failure_count} 次，触发熔断 "
                f"(冷却 {self.recovery_timeout}s)"
            )
            self.state = CircuitState.OPEN

    def record_slow(self, response_time: float):
        if response_time > self.slow_threshold:
            self.failure_count = min(self.failure_count + 0.5, self.failure_threshold)
            logger.info(
                f"[熔断器] {self.name} 慢请求 {response_time:.1f}s > {self.slow_threshold}s"
            )

    def _reset(self):
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.half_open_calls = 0

    @property
    def is_open(self) -> bool:
        return self.state == CircuitState.OPEN

    @property
    def success_rate(self) -> float:
        if self.total_requests == 0:
            return 100.0
        return (self.total_requests - self.error_requests) / self.total_requests * 100

    def get_status(self) -> dict:
        return {
            "name": self.name,
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_rate": round(self.success_rate, 1),
            "total_requests": self.total_requests,
            "error_requests": self.error_requests,
            "is_healthy": self.state == CircuitState.CLOSED,
        }


# ============================================================
# 限速检测器 (Rate Limit Detector)
# ============================================================
@dataclass
class RateLimitInfo:
    limit: int = 0
    remaining: int = 0
    reset_time: int = 0
    retry_after: int = 0
    is_limited: bool = False


@dataclass
class RateLimitDetector:
    """检测模型限速状态"""
    model_limits: Dict[str, RateLimitInfo] = field(default_factory=dict)
    low_water_mark: int = 3

    def update_from_response(self, model_id: str, status_code: int, headers: dict):
        info = RateLimitInfo(
            limit=int(headers.get("x-ratelimit-limit", 0)),
            remaining=int(headers.get("x-ratelimit-remaining", 999)),
            reset_time=int(headers.get("x-ratelimit-reset", 0)),
            retry_after=int(headers.get("retry-after", 0)),
        )
        if status_code == 429:
            info.is_limited = True
            logger.warning(f"[限速] {model_id} 收到 429，剩余 {info.remaining}，建议等待 {info.retry_after}s")
        elif info.remaining <= self.low_water_mark:
            info.is_limited = True
            logger.warning(f"[限速] {model_id} 剩余配额仅 {info.remaining}，标记为限速")
        self.model_limits[model_id] = info

    def is_limited(self, model_id: str) -> bool:
        info = self.model_limits.get(model_id)
        if not info:
            return False
        if not info.is_limited:
            return False
        # 检查是否过了重置时间
        if info.reset_time > 0 and time.time() > info.reset_time:
            info.is_limited = False
            return False
        return True

    def get_wait_time(self, model_id: str) -> int:
        info = self.model_limits.get(model_id)
        if not info or not info.is_limited:
            return 0
        wait = max(info.retry_after, info.reset_time - int(time.time()), 60)
        return wait


# ============================================================
# 模型信息
# ============================================================
@dataclass
class ModelInfo:
    model_id: str
    provider: str
    name: str
    strengths: List[str] = field(default_factory=list)
    priority: int = 10
    context_length: int = 131072
    is_free: bool = False
    score: float = 0.0


# ============================================================
# 消息分析器 (Message Analyzer)
# ============================================================
class MessageAnalyzer:
    """分析用户消息，判断任务类型"""

    CODE_PATTERNS = [
        r'```[\w]*\n', r'function\s+\w+', r'def\s+\w+', r'class\s+\w+',
        r'import\s+\w+', r'from\s+\w+\s+import', r'const\s+\w+\s*=',
        r'let\s+\w+\s*=', r'var\s+\w+\s*=', r'public\s+class',
        r'private\s+void', r'select\s+.*\s+from', r'CREATE\s+TABLE',
        r'<html', r'<div', r'style\s*=', r'println', r'console\.log',
        r'print\(', r'printf\(', r'system\.out', r'fmt\.Print',
        r'写一个.*函数', r'写一个.*脚本', r'帮我写.*代码', r'编程',
        r'写个.*程序', r'代码.*错误', r'bug', r'debug',
    ]

    REASONING_KEYWORDS = [
        r'分析', r'推理', r'逻辑', r'原因', r'为什么', r'如何',
        r'证明', r'推导', r'比较.*区别', r'优缺点', r'利弊',
        r'思考', r'explain', r'reason', r'analyze', r'why',
        r'how does', r'compare', r'derive', r'prove', r'evaluate',
        r'权衡', r'判断', r'评估', r'论证',
    ]

    @classmethod
    def analyze(cls, messages: list) -> dict:
        """分析消息，返回特征字典"""
        features = {
            "has_image": False,
            "language": "zh",
            "message_length": 0,
            "is_code": False,
            "is_reasoning": False,
            "has_long_context": False,
        }

        full_text = ""
        for msg in messages:
            content = msg.get("content", "")
            if isinstance(content, list):
                for part in content:
                    if isinstance(part, dict):
                        if part.get("type") == "image_url":
                            features["has_image"] = True
                        elif part.get("type") == "text":
                            full_text += part.get("text", "")
            elif isinstance(content, str):
                full_text += content

        features["message_length"] = len(full_text)
        features["has_long_context"] = features["message_length"] > 8000

        # 语言检测（简单启发式）
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', full_text))
        if chinese_chars > len(full_text) * 0.3:
            features["language"] = "zh"
        else:
            features["language"] = "en"

        # 代码检测
        for pattern in cls.CODE_PATTERNS:
            if re.search(pattern, full_text, re.IGNORECASE):
                features["is_code"] = True
                break

        # 推理检测
        for keyword in cls.REASONING_KEYWORDS:
            if re.search(keyword, full_text, re.IGNORECASE):
                features["is_reasoning"] = True
                break

        return features


# ============================================================
# 模型选择器 (Model Selector)
# ============================================================
class ModelSelector:
    """根据任务特征选择最优模型"""

    def __init__(self, models: Dict[str, ModelInfo], rules: list):
        self.models = models
        self.rules = rules

    def select(self, features: dict) -> List[str]:
        """根据消息特征返回排序后的模型候选列表"""
        candidates = []

        # 按规则匹配
        for rule in self.rules:
            if self._match_rule(rule, features):
                strategy = rule.get("autoStrategy", "")
                matched = self._select_by_strategy(strategy, features)
                candidates.extend(matched)
                # 加入 fallback
                fallback = rule.get("fallback", "")
                if fallback and fallback not in candidates:
                    candidates.append(fallback)

        # 补充：如果没有规则匹配，返回所有模型按优先级排序
        if not candidates:
            candidates = self._get_all_sorted()

        # 去重并保持顺序
        seen = set()
        unique = []
        for m in candidates:
            if m not in seen:
                seen.add(m)
                unique.append(m)
        return unique

    def _match_rule(self, rule: dict, features: dict) -> bool:
        condition = rule.get("condition", "")
        if "has_image == true" in condition and features.get("has_image"):
            return True
        if "code patterns" in condition and features.get("is_code"):
            return True
        if "reasoning keywords" in condition and features.get("is_reasoning"):
            if "message_length > 200" in condition and features.get("message_length", 0) <= 200:
                return False
            return True
        if "language == 'en'" in condition and features.get("language") == "en":
            if "message_length < 500" in condition and features.get("message_length", 0) >= 500:
                return False
            return True
        if "message_length > 8000" in condition and features.get("has_long_context"):
            return True
        if "language == 'zh'" in condition and features.get("language") == "zh":
            if "message_length > 500" in condition and features.get("message_length", 0) >= 500:
                return True
        return False

    def _select_by_strategy(self, strategy: str, features: dict) -> List[str]:
        strength_map = {
            "best_vision": ["vision", "multimodal", "image"],
            "best_coding": ["coding", "code"],
            "best_english": ["english", "general"],
            "best_reasoning": ["reasoning", "math", "logic"],
            "best_long_context": ["long_context"],
            "best_chinese": ["chinese", "general"],
        }
        target_strengths = strength_map.get(strategy, ["general"])

        scored = []
        for model_id, info in self.models.items():
            score = 0
            for s in target_strengths:
                if s in info.strengths:
                    score += 10
            # 免费模型优先
            if info.is_free:
                score += 5
            # 优先级越低越好
            score -= info.priority * 0.1
            # 评分加成
            score += info.score * 3
            if score > 0:
                scored.append((model_id, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [m[0] for m in scored]

    def _get_all_sorted(self) -> List[str]:
        """返回所有模型按优先级排序"""
        models = list(self.models.items())
        models.sort(key=lambda x: (x[1].priority, -x[1].score))
        return [m[0] for m in models]


# ============================================================
# 模型路由器 (Model Router) - 核心调度
# ============================================================
class ModelRouter:
    """统一模型路由器：整合所有服务商，智能调度"""

    def __init__(self, config: dict):
        self.config = config
        self.providers = config.get("providers", {})
        self.default_model = config.get("default", "")
        self.rules = config.get("rules", [])
        self.breakers: Dict[str, CircuitBreaker] = {}
        self.rate_detector = RateLimitDetector(
            low_water_mark=config.get("rateLimit", {}).get("lowWaterMark", 3)
        )
        self.models: Dict[str, ModelInfo] = {}
        self.selector: Optional[ModelSelector] = None
        self._init_models()
        self._init_breakers()
        self.selector = ModelSelector(self.models, self.rules)

    def _init_models(self):
        """初始化模型信息"""
        for provider_name, provider_cfg in self.providers.items():
            base_url = provider_cfg.get("baseUrl", "")
            for model_id, model_cfg in provider_cfg.get("models", {}).items():
                full_id = f"{provider_name}/{model_id}" if "/" not in model_id else model_id
                self.models[full_id] = ModelInfo(
                    model_id=model_id,
                    provider=provider_name,
                    name=model_cfg.get("name", model_id),
                    strengths=model_cfg.get("strengths", []),
                    priority=model_cfg.get("priority", 10),
                    is_free=":free" in model_id,
                    score=model_cfg.get("score", 0.0),
                )
        logger.info(f"已加载 {len(self.models)} 个模型")

    def _init_breakers(self):
        """为每个模型初始化熔断器"""
        cb_cfg = self.config.get("circuitBreaker", {})
        for model_id in self.models:
            self.breakers[model_id] = CircuitBreaker(
                name=model_id,
                failure_threshold=cb_cfg.get("failureThreshold", 3),
                recovery_timeout=cb_cfg.get("recoveryTimeout", 60),
                half_open_max_probes=cb_cfg.get("halfOpenMaxProbes", 1),
                slow_threshold=cb_cfg.get("slowThreshold", 25),
            )

    def get_provider_and_model(self, full_model_id: str) -> Tuple[str, str, str, str]:
        """解析模型ID，返回 (provider_name, actual_model_id, base_url, api_key)"""
        # 直接匹配 provider/model_id 格式
        for provider_name, provider_cfg in self.providers.items():
            if full_model_id.startswith(provider_name + "/"):
                actual_model = full_model_id[len(provider_name) + 1:]
                return (
                    provider_name,
                    actual_model,
                    provider_cfg.get("baseUrl", ""),
                    provider_cfg.get("apiKey", ""),
                )
        # 尝试在所有 provider 的 models 中查找
        for provider_name, provider_cfg in self.providers.items():
            if full_model_id in provider_cfg.get("models", {}):
                return (
                    provider_name,
                    full_model_id,
                    provider_cfg.get("baseUrl", ""),
                    provider_cfg.get("apiKey", ""),
                )
        raise ValueError(f"未找到模型: {full_model_id}")

    async def route(self, messages: list, requested_model: str = "") -> dict:
        """
        核心路由方法：分析消息 → 选择模型 → 调用（含熔断/限速/降级）
        返回: {"model": str, "provider": str, "response": Any}
        """
        # 1. 分析消息特征
        features = MessageAnalyzer.analyze(messages)

        # 2. 确定候选模型列表
        if requested_model and requested_model in self.models:
            candidates = [requested_model]
        elif requested_model:
            # 可能是 provider/model 格式
            candidates = [requested_model]
            # 同时加入智能路由候选
            candidates.extend(self.selector.select(features))
        else:
            candidates = self.selector.select(features)

        # 加入默认模型作为最后兜底
        if self.default_model and self.default_model not in candidates:
            candidates.append(self.default_model)

        logger.info(
            f"[路由] 消息长度={features['message_length']}, "
            f"语言={features['language']}, "
            f"代码={features['is_code']}, "
            f"推理={features['is_reasoning']}, "
            f"图片={features['has_image']}, "
            f"候选模型={len(candidates)}"
        )

        # 3. 依次尝试候选模型
        last_error = None
        for model_id in candidates:
            breaker = self.breakers.get(model_id)
            if breaker and breaker.is_open:
                logger.debug(f"[路由] {model_id} 熔断中，跳过")
                continue

            if self.rate_detector.is_limited(model_id):
                wait = self.rate_detector.get_wait_time(model_id)
                logger.debug(f"[路由] {model_id} 限速中(等待{wait}s)，跳过")
                continue

            try:
                result = await self._call_model(model_id, messages)
                return result
            except Exception as e:
                last_error = e
                logger.warning(f"[路由] {model_id} 调用失败: {e}")
                continue

        # 4. 全部失败
        error_msg = f"所有候选模型均失败: {last_error}"
        logger.error(f"[路由] {error_msg}")
        raise Exception(error_msg)

    async def _call_model(self, model_id: str, messages: list) -> dict:
        """调用单个模型（含熔断保护和限速检测）"""
        provider_name, actual_model, base_url, api_key = self.get_provider_and_model(model_id)
        breaker = self.breakers.get(model_id)

        if breaker and not breaker.can_execute():
            raise Exception(f"{model_id} 熔断中，无法执行")

        url = f"{base_url}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        payload = {
            "model": actual_model,
            "messages": messages,
            "stream": False,
        }

        timeout = self.config.get("circuitBreaker", {}).get("timeoutPerRequest", 30)
        start_time = time.time()

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(url, json=payload, headers=headers)
                elapsed = time.time() - start_time

            # 限速检测
            self.rate_detector.update_from_response(
                model_id, response.status_code, dict(response.headers)
            )
            if self.rate_detector.is_limited(model_id):
                if breaker:
                    breaker.record_failure("429", elapsed)
                raise Exception(f"{model_id} 被限速")

            # 错误处理
            if response.status_code == 429:
                if breaker:
                    breaker.record_failure("429", elapsed)
                raise Exception(f"{model_id} 返回 429 限速")
            if response.status_code == 402:
                if breaker:
                    breaker.record_failure("402", elapsed)
                raise Exception(f"{model_id} 余额不足 (402)")
            if response.status_code >= 500:
                if breaker:
                    breaker.record_failure(f"{response.status_code}", elapsed)
                raise Exception(f"{model_id} 服务错误 ({response.status_code})")

            response.raise_for_status()
            data = response.json()

            # 空响应检测
            choices = data.get("choices", [])
            if not choices:
                content = ""
                if breaker:
                    breaker.record_failure("empty_response", elapsed)
                raise Exception(f"{model_id} 返回空响应")

            content = choices[0].get("message", {}).get("content", "")
            if not content or not content.strip():
                if breaker:
                    breaker.record_failure("empty_response", elapsed)
                raise Exception(f"{model_id} 返回空内容")

            # 成功
            if breaker:
                breaker.record_success(elapsed)
                breaker.record_slow(elapsed)

            logger.info(
                f"[调用] {model_id} 成功 ({elapsed:.1f}s, "
                f"输出{len(content)}字)"
            )

            return {
                "model": model_id,
                "provider": provider_name,
                "response": data,
                "response_time": elapsed,
            }

        except httpx.TimeoutException:
            elapsed = time.time() - start_time
            if breaker:
                breaker.record_failure("timeout", elapsed)
            raise Exception(f"{model_id} 请求超时 ({elapsed:.1f}s)")
        except httpx.ConnectError as e:
            if breaker:
                breaker.record_failure("connect_error", 0)
            raise Exception(f"{model_id} 连接失败: {e}")

    async def route_stream(self, messages: list, requested_model: str = ""):
        """流式路由：返回生成器"""
        features = MessageAnalyzer.analyze(messages)

        if requested_model and requested_model in self.models:
            candidates = [requested_model]
        else:
            candidates = self.selector.select(features)

        if self.default_model and self.default_model not in candidates:
            candidates.append(self.default_model)

        last_error = None
        for model_id in candidates:
            breaker = self.breakers.get(model_id)
            if breaker and breaker.is_open:
                continue
            if self.rate_detector.is_limited(model_id):
                continue

            try:
                async for chunk in self._call_model_stream(model_id, messages):
                    yield chunk
                return
            except Exception as e:
                last_error = e
                logger.warning(f"[路由-流式] {model_id} 失败: {e}")
                continue

        # 全部失败，返回错误
        error_data = {
            "error": {
                "message": f"所有候选模型均失败: {last_error}",
                "type": "router_error",
                "code": "all_models_failed",
            }
        }
        yield f"data: {json.dumps(error_data)}\n\n"
        yield "data: [DONE]\n\n"

    async def _call_model_stream(self, model_id: str, messages: list):
        """流式调用单个模型"""
        provider_name, actual_model, base_url, api_key = self.get_provider_and_model(model_id)
        breaker = self.breakers.get(model_id)

        if breaker and not breaker.can_execute():
            raise Exception(f"{model_id} 熔断中")

        url = f"{base_url}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        payload = {
            "model": actual_model,
            "messages": messages,
            "stream": True,
        }

        timeout = self.config.get("server", {}).get("requestTimeout", 120)
        start_time = time.time()
        has_content = False

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                async with client.stream("POST", url, json=payload, headers=headers) as response:
                    # 限速检测
                    self.rate_detector.update_from_response(
                        model_id, response.status_code, dict(response.headers)
                    )

                    if response.status_code == 429:
                        if breaker:
                            breaker.record_failure("429", 0)
                        raise Exception(f"{model_id} 被限速")
                    if response.status_code >= 500:
                        if breaker:
                            breaker.record_failure(f"{response.status_code}", 0)
                        raise Exception(f"{model_id} 服务错误 ({response.status_code})")

                    async for line in response.aiter_lines():
                        if not line.strip():
                            continue
                        if line.startswith("data: "):
                            data_str = line[6:]
                            if data_str.strip() == "[DONE]":
                                break
                            try:
                                chunk_data = json.loads(data_str)
                                has_content = True
                                # 替换模型名为路由模型名
                                if "model" in chunk_data:
                                    chunk_data["model"] = model_id
                                yield f"data: {json.dumps(chunk_data)}\n\n"
                            except json.JSONDecodeError:
                                continue

            elapsed = time.time() - start_time

            if not has_content:
                if breaker:
                    breaker.record_failure("empty_response", elapsed)
                raise Exception(f"{model_id} 流式返回空内容")

            if breaker:
                breaker.record_success(elapsed)

            logger.info(f"[调用-流式] {model_id} 成功 ({elapsed:.1f}s)")

        except httpx.TimeoutException:
            elapsed = time.time() - start_time
            if breaker:
                breaker.record_failure("timeout", elapsed)
            raise
        except httpx.ConnectError as e:
            if breaker:
                breaker.record_failure("connect_error", 0)
            raise

    def get_status(self) -> dict:
        """获取路由器整体状态"""
        breaker_statuses = {}
        for model_id, breaker in self.breakers.items():
            breaker_statuses[model_id] = breaker.get_status()

        rate_limit_statuses = {}
        for model_id, info in self.rate_detector.model_limits.items():
            rate_limit_statuses[model_id] = {
                "remaining": info.remaining,
                "is_limited": info.is_limited,
            }

        healthy_count = sum(1 for b in self.breakers.values() if not b.is_open)
        total_count = len(self.breakers)

        return {
            "total_models": total_count,
            "healthy_models": healthy_count,
            "open_circuits": total_count - healthy_count,
            "breakers": breaker_statuses,
            "rate_limits": rate_limit_statuses,
        }


# ============================================================
# 自动更新器 (Auto Updater)
# ============================================================
class AutoUpdater:
    """每天自动更新 OpenRouter 免费模型列表"""

    OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"

    def __init__(self, config: dict, router: ModelRouter):
        self.config = config
        self.router = router
        self.au_cfg = config.get("autoUpdate", {})
        self.blocklist = set(self.au_cfg.get("blocklist", []))
        self.min_context = self.au_cfg.get("minContextWindow", 32000)
        self.min_score = self.au_cfg.get("minScore", 0.5)
        self.max_models = self.au_cfg.get("maxFreeModels", 10)

    async def update(self):
        """执行模型列表更新"""
        if not self.au_cfg.get("enabled", False):
            logger.info("[自动更新] 已禁用，跳过")
            return

        logger.info("[自动更新] 开始更新 OpenRouter 免费模型列表...")

        try:
            # 1. 拉取 OpenRouter 模型列表
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(self.OPENROUTER_MODELS_URL)
                response.raise_for_status()
                data = response.json()

            all_models = data.get("data", [])
            logger.info(f"[自动更新] OpenRouter 共 {len(all_models)} 个模型")

            # 2. 筛选免费模型
            free_models = []
            for m in all_models:
                model_id = m.get("id", "")
                pricing = m.get("pricing", {})
                prompt_price = pricing.get("prompt", "1")
                completion_price = pricing.get("completion", "1")

                # 检查是否真正免费
                try:
                    if float(prompt_price) > 0 or float(completion_price) > 0:
                        continue
                except (ValueError, TypeError):
                    continue

                # 检查黑名单
                if model_id in self.blocklist:
                    continue

                # 检查上下文长度
                context_length = m.get("context_length", 0)
                if context_length < self.min_context:
                    continue

                # 计算评分
                score = self._score_model(m)
                if score < self.min_score:
                    continue

                free_models.append({
                    "id": model_id,
                    "name": m.get("name", model_id),
                    "context_length": context_length,
                    "score": score,
                    "strengths": self._infer_strengths(m),
                })

            # 3. 按评分排序，取前 N 个
            free_models.sort(key=lambda x: x["score"], reverse=True)
            selected = free_models[:self.max_models]

            logger.info(
                f"[自动更新] 筛选出 {len(free_models)} 个合格免费模型，"
                f"选取前 {len(selected)} 个"
            )

            # 4. 更新路由器模型池
            for m in selected:
                model_id = m["id"]
                self.router.models[model_id] = ModelInfo(
                    model_id=model_id,
                    provider="openrouter",
                    name=m["name"],
                    strengths=m["strengths"],
                    priority=1,
                    context_length=m["context_length"],
                    is_free=True,
                    score=m["score"],
                )
                # 初始化熔断器
                if model_id not in self.router.breakers:
                    cb_cfg = self.config.get("circuitBreaker", {})
                    self.router.breakers[model_id] = CircuitBreaker(
                        name=model_id,
                        failure_threshold=cb_cfg.get("failureThreshold", 3),
                        recovery_timeout=cb_cfg.get("recoveryTimeout", 60),
                    )

            # 5. 重新初始化选择器
            self.router.selector = ModelSelector(self.router.models, self.router.rules)

            # 6. 更新配置文件中的 openrouter models
            self._update_config_file(selected)

            logger.info(
                f"[自动更新] 完成！更新模型: "
                f"{', '.join(m['id'] for m in selected[:5])}"
                f"{'...' if len(selected) > 5 else ''}"
            )

        except Exception as e:
            logger.error(f"[自动更新] 失败: {e}")

    def _score_model(self, model: dict) -> float:
        """为模型评分"""
        score = 0.0
        context_length = model.get("context_length", 0)

        # 上下文长度评分 (0-30分)
        if context_length >= 128000:
            score += 30
        elif context_length >= 64000:
            score += 25
        elif context_length >= 32000:
            score += 20
        else:
            score += 10

        # 架构评分 (0-25分)
        name = model.get("id", "").lower()
        if "deepseek" in name or "qwen" in name:
            score += 25
        elif "llama" in name and ("70b" in name or "72b" in name or "8b" not in name):
            score += 22
        elif "gemma" in name:
            score += 20
        elif "mistral" in name or "mixtral" in name:
            score += 18
        elif "glm" in name or "chatglm" in name:
            score += 20
        elif "phi" in name:
            score += 15
        else:
            score += 10

        # 能力评分 (0-25分)
        if "coder" in name or "code" in name:
            score += 10
        if "vision" in name or "vl" in name:
            score += 8
        if "reasoning" in name or "r1" in name:
            score += 10
        if "instruct" in name:
            score += 5

        # 知名度评分 (0-20分)
        if model.get("top_provider", {}).get("is_moderated", False):
            score += 10
        if context_length >= 100000:
            score += 10
        elif context_length >= 60000:
            score += 5

        return round(score, 1)

    def _infer_strengths(self, model: dict) -> List[str]:
        """推断模型擅长领域"""
        name = model.get("id", "").lower()
        strengths = ["general"]
        if "code" in name or "coder" in name:
            strengths.extend(["coding", "code"])
        if "vision" in name or "vl" in name:
            strengths.extend(["vision", "multimodal"])
        if "reason" in name or "r1" in name:
            strengths.extend(["reasoning", "math"])
        if "deepseek" in name or "qwen" in name:
            strengths.append("chinese")
        if "gemma" in name or "llama" in name:
            strengths.append("english")
        if model.get("context_length", 0) >= 100000:
            strengths.append("long_context")
        return list(set(strengths))

    def _update_config_file(self, selected_models: list):
        """更新配置文件中的 openrouter models"""
        try:
            config_path = CONFIG_PATH
            with open(config_path, "r", encoding="utf-8") as f:
                content = f.read()

            config = json.loads(content)
            if "providers" in config and "openrouter" in config["providers"]:
                new_models = {}
                for m in selected_models:
                    new_models[m["id"]] = {
                        "name": m["name"],
                        "strengths": m["strengths"],
                        "priority": 1,
                        "score": m["score"],
                    }
                config["providers"]["openrouter"]["models"] = new_models
                config["updateAt"] = datetime.utcnow().isoformat() + "Z"

                with open(config_path, "w", encoding="utf-8") as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)

                logger.info("[自动更新] 配置文件已更新")
        except Exception as e:
            logger.warning(f"[自动更新] 配置文件更新失败: {e}")


# ============================================================
# FastAPI 应用
# ============================================================
app = FastAPI(title="统一模型路由网关", version="1.0.0")

# 全局路由器实例
router_instance: Optional[ModelRouter] = None
updater_instance: Optional[AutoUpdater] = None


@app.on_event("startup")
async def startup_event():
    global router_instance, updater_instance
    config = load_config(CONFIG_PATH)
    router_instance = ModelRouter(config)
    updater_instance = AutoUpdater(config, router_instance)

    # 启动时执行一次自动更新
    if config.get("autoUpdate", {}).get("enabled", False):
        asyncio.create_task(updater_instance.update())

    # 启动定时更新任务
    schedule = config.get("autoUpdate", {}).get("schedule", "0 5 * * *")
    asyncio.create_task(scheduled_update(schedule))

    logger.info("🚀 统一模型路由网关启动完成")


async def scheduled_update(cron_expr: str):
    """定时执行自动更新（解析 cron 表达式）"""
    parts = cron_expr.split()
    if len(parts) != 5:
        logger.warning(f"[定时任务] 无效的 cron 表达式: {cron_expr}")
        return

    minute, hour, _, _, _ = parts
    target_minute = int(minute)
    target_hour = int(hour)

    while True:
        now = datetime.now()
        # 每分钟检查一次
        if now.hour == target_hour and now.minute == target_minute:
            logger.info("[定时任务] 开始执行每日自动更新")
            await updater_instance.update()
            # 等到下一分钟，避免重复执行
            await asyncio.sleep(60)
        else:
            await asyncio.sleep(30)


# ============================================================
# API 请求/响应模型
# ============================================================
class ChatMessage(BaseModel):
    role: str
    content: Any = None


class ChatCompletionRequest(BaseModel):
    model: str = ""
    messages: List[ChatMessage]
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False
    top_p: Optional[float] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None


# ============================================================
# API 端点
# ============================================================
@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    """OpenAI 兼容的聊天补全接口"""
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="无效的 JSON 请求体")

    messages = body.get("messages", [])
    requested_model = body.get("model", "")
    is_stream = body.get("stream", False)

    if not messages:
        raise HTTPException(status_code=400, detail="messages 不能为空")

    if is_stream:
        return StreamingResponse(
            router_instance.route_stream(messages, requested_model),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )

    # 非流式
    try:
        result = await router_instance.route(messages, requested_model)
        response_data = result["response"]
        # 替换模型名
        response_data["model"] = result["model"]
        return JSONResponse(content=response_data)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@app.get("/v1/models")
async def list_models():
    """列出所有可用模型"""
    models = []
    for model_id, info in router_instance.models.items():
        breaker = router_instance.breakers.get(model_id)
        rate_info = router_instance.rate_detector.model_limits.get(model_id)
        models.append({
            "id": model_id,
            "object": "model",
            "owned_by": info.provider,
            "name": info.name,
            "strengths": info.strengths,
            "is_free": info.is_free,
            "priority": info.priority,
            "score": info.score,
            "healthy": breaker.is_open is False if breaker else True,
            "rate_limited": rate_info.is_limited if rate_info else False,
        })
    return JSONResponse(content={
        "object": "list",
        "data": models,
        "total": len(models),
    })


@app.get("/v1/status")
async def get_status():
    """获取路由器状态（熔断器、限速、健康度）"""
    status = router_instance.get_status()
    return JSONResponse(content=status)


@app.get("/v1/status/breakers")
async def get_breaker_status():
    """获取所有熔断器状态"""
    breakers = {}
    for model_id, breaker in router_instance.breakers.items():
        breakers[model_id] = breaker.get_status()
    return JSONResponse(content=breakers)


@app.get("/v1/status/rate-limits")
async def get_rate_limit_status():
    """获取所有限速状态"""
    limits = {}
    for model_id, info in router_instance.rate_detector.model_limits.items():
        limits[model_id] = {
            "remaining": info.remaining,
            "limit": info.limit,
            "is_limited": info.is_limited,
            "wait_time": router_instance.rate_detector.get_wait_time(model_id),
        }
    return JSONResponse(content=limits)


@app.post("/v1/update/now")
async def trigger_update():
    """手动触发模型列表更新"""
    if updater_instance:
        asyncio.create_task(updater_instance.update())
        return JSONResponse(content={"status": "ok", "message": "更新任务已启动"})
    return JSONResponse(content={"status": "error", "message": "自动更新未启用"})


@app.post("/v1/breaker/reset/{model_id}")
async def reset_breaker(model_id: str):
    """手动重置指定模型的熔断器"""
    breaker = router_instance.breakers.get(model_id)
    if breaker:
        breaker._reset()
        return JSONResponse(content={"status": "ok", "message": f"{model_id} 熔断器已重置"})
    return JSONResponse(content={"status": "error", "message": f"未找到 {model_id} 的熔断器"})


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return JSONResponse(content={"status": "ok", "timestamp": datetime.utcnow().isoformat()})


# ============================================================
# 启动入口
# ============================================================
if __name__ == "__main__":
    server_cfg = {}
    try:
        config = load_config(CONFIG_PATH)
        server_cfg = config.get("server", {})
    except Exception:
        pass

    host = server_cfg.get("host", "0.0.0.0")
    port = server_cfg.get("port", 19000)
    log_level = server_cfg.get("logLevel", "info")

    logger.info(f"🌐 启动统一模型路由网关: http://{host}:{port}")
    logger.info(f"📖 API 文档: http://{host}:{port}/docs")
    logger.info(f"🔧 状态面板: http://{host}:{port}/v1/status")

    uvicorn.run(
        "server:app",
        host=host,
        port=port,
        log_level=log_level,
        reload=False,
    )
