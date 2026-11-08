#!/usr/bin/env python3
"""
东方智慧智能体集成测试脚本
测试 OpenClaw & Hermes Agent 集成
"""

import os
import sys
import time
import requests
import json
from datetime import datetime

# 颜色定义
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

API_BASE = "http://localhost:5000"


def print_header(text):
    print()
    print(BOLD + "=" * 60 + RESET)
    print(BOLD + BLUE + f"  {text}" + RESET)
    print(BOLD + "=" * 60 + RESET)


def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")


def print_error(text):
    print(f"{RED}❌ {text}{RESET}")


def print_info(text):
    print(f"{BLUE}ℹ️  {text}{RESET}")


def print_warning(text):
    print(f"{YELLOW}⚠️  {text}{RESET}")


class IntegrationTester:
    """集成测试器"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.api_available = False
    
    def run_all_tests(self):
        """运行所有测试"""
        print_header("东方智慧智能体集成测试")
        print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"API地址: {API_BASE}")
        
        # 1. API连接测试
        self.test_api_connection()
        
        if not self.api_available:
            print_error("API服务未启动，请先运行: python integration/api_server.py")
            return
        
        # 2. 健康检查
        self.test_health_check()
        
        # 3. 商道智能测试
        self.test_commercial_opportunity()
        self.test_commercial_investment()
        self.test_commercial_strategy()
        self.test_commercial_wisdom()
        self.test_commercial_advice()
        self.test_commercial_report()
        
        # 4. 形象系统测试
        self.test_avatar_presets()
        self.test_avatar_create()
        self.test_avatar_adjust()
        self.test_avatar_render()
        
        # 5. 状态检查
        self.test_status()
        
        # 6. OpenClaw Webhook
        self.test_openclaw_webhook()
        
        # 7. Hermes 接口
        self.test_hermes_commercial()
        self.test_hermes_avatar()
        
        # 汇总结果
        self.print_summary()
    
    def test_api_connection(self):
        """测试API连接"""
        print_header("1. API连接测试")
        try:
            response = requests.get(f"{API_BASE}/health", timeout=5)
            if response.status_code == 200:
                print_success(f"API服务正常运行")
                self.api_available = True
                self.passed += 1
            else:
                print_error(f"API返回异常状态码: {response.status_code}")
                self.failed += 1
        except requests.exceptions.ConnectionError:
            print_error("无法连接到API服务")
            print_info("请确保已启动API服务: python integration/api_server.py")
            self.failed += 1
        except Exception as e:
            print_error(f"连接错误: {e}")
            self.failed += 1
    
    def test_health_check(self):
        """测试健康检查"""
        print_header("2. 健康检查")
        try:
            response = requests.get(f"{API_BASE}/health", timeout=5)
            data = response.json()
            
            checks = [
                ("status", data.get("status") == "ok"),
                ("service", "Oriental Wisdom" in data.get("service", "")),
                ("version", "version" in data)
            ]
            
            for name, result in checks:
                if result:
                    print_success(f"健康检查 - {name}: OK")
                    self.passed += 1
                else:
                    print_error(f"健康检查 - {name}: FAIL")
                    self.failed += 1
                    
        except Exception as e:
            print_error(f"健康检查失败: {e}")
            self.failed += 3
    
    def test_commercial_opportunity(self):
        """测试商机分析"""
        print_header("3.1 商道 - 商机分析")
        try:
            data = {
                "unmet_needs": ["智能家居"],
                "technology_trends": ["AI", "IoT"]
            }
            response = requests.post(f"{API_BASE}/api/commercial/opportunity", json=data, timeout=10)
            result = response.json()
            
            if result.get("total_count", 0) > 0:
                print_success(f"商机分析: 识别到 {result['total_count']} 个商机")
                self.passed += 1
            else:
                print_warning("商机分析: 未识别到商机（可能正常）")
                self.passed += 1
                
        except Exception as e:
            print_error(f"商机分析失败: {e}")
            self.failed += 1
    
    def test_commercial_investment(self):
        """测试投资分析"""
        print_header("3.2 商道 - 投资分析")
        try:
            data = {
                "name": "AI产品研发",
                "initial_investment": 2000000,
                "annual_cash_flows": [600000, 800000, 1000000, 900000],
                "risk_level": "MEDIUM"
            }
            response = requests.post(f"{API_BASE}/api/commercial/investment", json=data, timeout=10)
            result = response.json()
            
            checks = [
                ("project_name", result.get("project_name") == "AI产品研发"),
                ("roi", "roi" in result),
                ("recommendation", "recommendation" in result)
            ]
            
            for name, result_check in checks:
                if result_check:
                    print_success(f"投资分析 - {name}: OK")
                    self.passed += 1
                else:
                    print_error(f"投资分析 - {name}: FAIL")
                    self.failed += 1
            
            print_info(f"   ROI: {result.get('roi', 0):.0%}")
            print_info(f"   建议: {result.get('recommendation', 'N/A')[:40]}...")
                
        except Exception as e:
            print_error(f"投资分析失败: {e}")
            self.failed += 3
    
    def test_commercial_strategy(self):
        """测试战略规划"""
        print_header("3.3 商道 - 战略规划")
        try:
            data = {
                "industry": "科技",
                "strategy_type": "differentiation"
            }
            response = requests.post(f"{API_BASE}/api/commercial/strategy", json=data, timeout=10)
            result = response.json()
            
            if result.get("vision"):
                print_success("战略规划: 生成成功")
                self.passed += 1
            else:
                print_error("战略规划: 生成失败")
                self.failed += 1
                
        except Exception as e:
            print_error(f"战略规划失败: {e}")
            self.failed += 1
    
    def test_commercial_wisdom(self):
        """测试商道智慧"""
        print_header("3.4 商道 - 东方智慧")
        try:
            response = requests.get(f"{API_BASE}/api/commercial/wisdom", timeout=10)
            result = response.json()
            
            insights = result.get("insights", [])
            if len(insights) > 0:
                print_success(f"商道智慧: 获取到 {len(insights)} 条智慧")
                self.passed += 1
            else:
                print_error("商道智慧: 获取失败")
                self.failed += 1
                
        except Exception as e:
            print_error(f"商道智慧获取失败: {e}")
            self.failed += 1
    
    def test_commercial_advice(self):
        """测试商道建议"""
        print_header("3.5 商道 - 场景建议")
        try:
            situations = ["startup", "growth", "mature"]
            for situation in situations:
                response = requests.get(
                    f"{API_BASE}/api/commercial/advice",
                    params={"situation": situation},
                    timeout=10
                )
                result = response.json()
                
                if result.get("advice"):
                    print_success(f"场景建议 - {situation}: OK")
                    self.passed += 1
                else:
                    print_error(f"场景建议 - {situation}: FAIL")
                    self.failed += 1
                
        except Exception as e:
            print_error(f"场景建议失败: {e}")
            self.failed += 3
    
    def test_commercial_report(self):
        """测试综合报告"""
        print_header("3.6 商道 - 综合报告")
        try:
            data = {
                "title": "测试商业分析",
                "market_data": {"unmet_needs": ["测试"]},
                "strategy_data": {"industry": "测试"}
            }
            response = requests.post(f"{API_BASE}/api/commercial/report", json=data, timeout=10)
            result = response.json()
            
            if result.get("report_id"):
                print_success("综合报告: 生成成功")
                self.passed += 1
            else:
                print_error("综合报告: 生成失败")
                self.failed += 1
                
        except Exception as e:
            print_error(f"综合报告失败: {e}")
            self.failed += 1
    
    def test_avatar_presets(self):
        """测试形象预设"""
        print_header("4.1 形象 - 预设列表")
        try:
            response = requests.get(f"{API_BASE}/api/avatar/presets", timeout=10)
            result = response.json()
            
            presets = result.get("presets", [])
            if len(presets) >= 5:
                print_success(f"形象预设: {len(presets)} 个预设可用")
                self.passed += 1
            else:
                print_error(f"形象预设: 只有 {len(presets)} 个预设")
                self.failed += 1
                
        except Exception as e:
            print_error(f"形象预设获取失败: {e}")
            self.failed += 1
    
    def test_avatar_create(self):
        """测试创建形象"""
        print_header("4.2 形象 - 创建形象")
        try:
            data = {"preset_id": "model_a", "name": "测试形象"}
            response = requests.post(f"{API_BASE}/api/avatar/create", json=data, timeout=10)
            result = response.json()
            
            if result.get("success") and result.get("avatar_id"):
                print_success(f"形象创建: {result.get('name')} (ID: {result['avatar_id'][:8]}...)")
                self.avatar_id = result["avatar_id"]
                self.passed += 1
            else:
                print_error("形象创建: 失败")
                self.failed += 1
                
        except Exception as e:
            print_error(f"形象创建失败: {e}")
            self.failed += 1
    
    def test_avatar_adjust(self):
        """测试微调形象"""
        print_header("4.3 形象 - 微调特征")
        try:
            if not hasattr(self, 'avatar_id'):
                print_warning("跳过微调测试（需要先创建形象）")
                return
            
            adjustments = [
                ("facial_features.eye_size", 0.65),
                ("hair_features.color", "#1a1a1a"),
                ("makeup_features.lipstick_color", "#d47575")
            ]
            
            for feature, value in adjustments:
                data = {
                    "avatar_id": self.avatar_id,
                    "feature": feature,
                    "value": value
                }
                response = requests.post(f"{API_BASE}/api/avatar/adjust", json=data, timeout=10)
                result = response.json()
                
                if result.get("success"):
                    print_success(f"微调 {feature.split('.')[-1]}: OK")
                    self.passed += 1
                else:
                    print_error(f"微调 {feature.split('.')[-1]}: FAIL")
                    self.failed += 1
                
        except Exception as e:
            print_error(f"微调失败: {e}")
            self.failed += 3
    
    def test_avatar_render(self):
        """测试渲染形象"""
        print_header("4.4 形象 - SVG渲染")
        try:
            if not hasattr(self, 'avatar_id'):
                print_warning("跳过渲染测试（需要先创建形象）")
                return
            
            response = requests.get(
                f"{API_BASE}/api/avatar/render",
                params={"avatar_id": self.avatar_id},
                timeout=10
            )
            
            if response.status_code == 200 and "svg" in response.headers.get("Content-Type", ""):
                print_success(f"SVG渲染: {len(response.content)} 字节")
                self.passed += 1
            else:
                print_error("SVG渲染: 返回格式异常")
                self.failed += 1
                
        except Exception as e:
            print_error(f"渲染失败: {e}")
            self.failed += 1
    
    def test_status(self):
        """测试状态获取"""
        print_header("5. 状态检查")
        try:
            response = requests.get(f"{API_BASE}/api/status", timeout=10)
            result = response.json()
            
            if "agent" in result and "commercial" in result:
                print_success("状态获取: 正常")
                commercial = result.get("commercial", {})
                print_info(f"   商道分析次数: {commercial.get('analysis_count', 0)}")
                print_info(f"   商机识别数: {commercial.get('opportunities_identified', 0)}")
                self.passed += 1
            else:
                print_error("状态获取: 格式异常")
                self.failed += 1
                
        except Exception as e:
            print_error(f"状态检查失败: {e}")
            self.failed += 1
    
    def test_openclaw_webhook(self):
        """测试OpenClaw Webhook"""
        print_header("6. OpenClaw Webhook")
        try:
            data = {
                "text": "分析AI商机",
                "user_id": "test_user",
                "chat_id": "test_chat"
            }
            response = requests.post(f"{API_BASE}/webhook/openclaw", json=data, timeout=15)
            result = response.json()
            
            if result.get("success"):
                print_success("OpenClaw Webhook: 响应正常")
                self.passed += 1
            else:
                print_error("OpenClaw Webhook: 响应异常")
                self.failed += 1
                
        except Exception as e:
            print_error(f"OpenClaw Webhook失败: {e}")
            self.failed += 1
    
    def test_hermes_commercial(self):
        """测试Hermes商业接口"""
        print_header("7.1 Hermes - 商道接口")
        try:
            data = {
                "action": "opportunity",
                "data": {"unmet_needs": ["测试"]}
            }
            response = requests.post(f"{API_BASE}/hermes/commercial", json=data, timeout=10)
            result = response.json()
            
            if "total_count" in result or "error" not in result:
                print_success("Hermes商道接口: 正常")
                self.passed += 1
            else:
                print_error("Hermes商道接口: 响应异常")
                self.failed += 1
                
        except Exception as e:
            print_error(f"Hermes商道接口失败: {e}")
            self.failed += 1
    
    def test_hermes_avatar(self):
        """测试Hermes形象接口"""
        print_header("7.2 Hermes - 形象接口")
        try:
            data = {"action": "list"}
            response = requests.post(f"{API_BASE}/hermes/avatar", json=data, timeout=10)
            result = response.json()
            
            if "presets" in result:
                print_success("Hermes形象接口: 正常")
                self.passed += 1
            else:
                print_error("Hermes形象接口: 响应异常")
                self.failed += 1
                
        except Exception as e:
            print_error(f"Hermes形象接口失败: {e}")
            self.failed += 1
    
    def print_summary(self):
        """打印测试汇总"""
        print()
        print_header("测试结果汇总")
        
        total = self.passed + self.failed
        pass_rate = (self.passed / total * 100) if total > 0 else 0
        
        print(f"{BOLD}总测试数: {total}{RESET}")
        print(f"{GREEN}通过: {self.passed}{RESET}")
        print(f"{RED}失败: {self.failed}{RESET}")
        print(f"{BOLD}通过率: {pass_rate:.1f}%{RESET}")
        
        print()
        if self.failed == 0:
            print_success("🎉 所有测试通过！集成成功！")
            print()
            print_info("下一步操作:")
            print("  1. OpenClaw 配置: cp integration/openclaw_config.json ~/.openclaw/")
            print("  2. Hermes 配置: cp integration/hermes_config.yaml ~/.hermes/")
            print("  3. 重启服务进行联调测试")
        else:
            print_warning(f"有 {self.failed} 个测试失败，请检查配置")
        
        print()


def main():
    """主函数"""
    tester = IntegrationTester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
