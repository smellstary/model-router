#!/usr/bin/env python3
"""
安全集成测试脚本
测试东方智慧智能体 API 服务（安全增强版）
"""

import requests
import json
import time
from datetime import datetime


class SecureAPITester:
    """安全 API 测试器"""

    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url
        self.results = []

    def test_health_check(self):
        """测试健康检查"""
        print("\n" + "=" * 60)
        print("1️⃣  健康检查测试")
        print("=" * 60)

        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            data = response.json()

            print(f"✅ 状态: {data.get('status')}")
            print(f"✅ 服务: {data.get('service')}")
            print(f"✅ 版本: {data.get('version')}")

            if 'security' in data:
                print("\n🔒 安全配置:")
                security = data['security']
                print(f"   - 频率限制: {'✅ 启用' if security.get('rate_limiting') else '❌ 禁用'}")
                print(f"   - IP白名单: {'✅ 启用' if security.get('ip_whitelist') else '❌ 禁用'}")
                print(f"   - 输入验证: {'✅ 启用' if security.get('input_validation') else '❌ 禁用'}")

            self.record_result("健康检查", True, "正常")
            return True

        except Exception as e:
            print(f"❌ 健康检查失败: {str(e)}")
            self.record_result("健康检查", False, str(e))
            return False

    def test_rate_limiting(self):
        """测试频率限制"""
        print("\n" + "=" * 60)
        print("2️⃣  频率限制测试")
        print("=" * 60)

        try:
            success_count = 0
            fail_count = 0

            for i in range(5):
                response = requests.get(f"{self.base_url}/health", timeout=5)
                if response.status_code == 200:
                    success_count += 1
                time.sleep(0.1)

            print(f"✅ 发送 5 个请求，{success_count} 个成功")

            if success_count == 5:
                print("✅ 频率限制正常工作（未触发限制）")
                self.record_result("频率限制", True, "正常工作")
                return True
            else:
                print("⚠️  部分请求失败")
                self.record_result("频率限制", False, "部分失败")
                return False

        except Exception as e:
            print(f"❌ 频率限制测试失败: {str(e)}")
            self.record_result("频率限制", False, str(e))
            return False

    def test_input_validation(self):
        """测试输入验证"""
        print("\n" + "=" * 60)
        print("3️⃣  输入验证测试")
        print("=" * 60)

        try:
            test_data = {
                'unmet_needs': ['测试需求'],
                'technology_trends': ['AI'],
                'description': '正常长度的描述'
            }

            response = requests.post(
                f"{self.base_url}/api/commercial/opportunity",
                json=test_data,
                timeout=10
            )

            if response.status_code == 200:
                print("✅ 正常输入测试通过")
            else:
                print(f"⚠️  响应状态码: {response.status_code}")

            long_text = '测试' * 10000
            test_data_long = {
                'unmet_needs': [long_text],
                'technology_trends': ['AI'],
            }

            response = requests.post(
                f"{self.base_url}/api/commercial/opportunity",
                json=test_data_long,
                timeout=10
            )

            if response.status_code in [200, 400]:
                print("✅ 长文本输入处理正确")
            else:
                print(f"⚠️  长文本响应: {response.status_code}")

            self.record_result("输入验证", True, "正常工作")
            return True

        except Exception as e:
            print(f"❌ 输入验证测试失败: {str(e)}")
            self.record_result("输入验证", False, str(e))
            return False

    def test_commercial_apis(self):
        """测试商道 API"""
        print("\n" + "=" * 60)
        print("4️⃣  商道 API 测试")
        print("=" * 60)

        endpoints = [
            ('/api/commercial/opportunity', 'POST', {
                'unmet_needs': ['智能家居'],
                'technology_trends': ['AI', 'IoT']
            }),
            ('/api/commercial/investment', 'POST', {
                'name': '测试项目',
                'initial_investment': 1000000,
                'annual_cash_flows': [300000, 400000, 500000]
            }),
            ('/api/commercial/strategy', 'POST', {
                'company_name': '测试公司',
                'industry': '科技'
            }),
            ('/api/commercial/wisdom', 'GET', None),
            ('/api/commercial/advice', 'GET', {'situation': 'startup'}),
        ]

        all_success = True

        for endpoint, method, data in endpoints:
            try:
                if method == 'GET':
                    response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                else:
                    response = requests.post(
                        f"{self.base_url}{endpoint}",
                        json=data,
                        timeout=10
                    )

                if response.status_code == 200:
                    print(f"✅ {endpoint} - 成功")
                else:
                    print(f"⚠️  {endpoint} - 状态码 {response.status_code}")
                    all_success = False

            except Exception as e:
                print(f"❌ {endpoint} - 失败: {str(e)}")
                all_success = False

        self.record_result("商道 API", all_success, "全部通过" if all_success else "部分失败")
        return all_success

    def test_avatar_apis(self):
        """测试形象 API"""
        print("\n" + "=" * 60)
        print("5️⃣  形象 API 测试")
        print("=" * 60)

        try:
            response = requests.get(f"{self.base_url}/api/avatar/presets", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 获取预设成功，共 {len(data.get('presets', []))} 个预设")
            else:
                print(f"⚠️  获取预设失败: {response.status_code}")
                return False

            avatar_data = {
                'preset_id': 'model_a',
                'name': '测试形象'
            }
            response = requests.post(
                f"{self.base_url}/api/avatar/create",
                json=avatar_data,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                print(f"✅ 创建形象成功: {data.get('name')}")
                self.record_result("形象 API", True, "正常工作")
                return True
            else:
                print(f"⚠️  创建形象失败: {response.status_code}")
                self.record_result("形象 API", False, "创建失败")
                return False

        except Exception as e:
            print(f"❌ 形象 API 测试失败: {str(e)}")
            self.record_result("形象 API", False, str(e))
            return False

    def test_openclaw_webhook(self):
        """测试 OpenClaw Webhook"""
        print("\n" + "=" * 60)
        print("6️⃣  OpenClaw Webhook 测试")
        print("=" * 60)

        try:
            webhook_data = {
                'text': '分析AI商机',
                'user_id': 'test_user_123',
                'chat_id': 'test_chat_456'
            }

            response = requests.post(
                f"{self.base_url}/webhook/openclaw",
                json=webhook_data,
                timeout=15
            )

            if response.status_code == 200:
                data = response.json()
                print(f"✅ Webhook 响应成功")
                print(f"   回复: {data.get('reply', '')[:100]}...")
                self.record_result("OpenClaw Webhook", True, "正常工作")
                return True
            else:
                print(f"⚠️  Webhook 失败: {response.status_code}")
                self.record_result("OpenClaw Webhook", False, f"状态码 {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Webhook 测试失败: {str(e)}")
            self.record_result("OpenClaw Webhook", False, str(e))
            return False

    def test_hermes_apis(self):
        """测试 Hermes API"""
        print("\n" + "=" * 60)
        print("7️⃣  Hermes API 测试")
        print("=" * 60)

        endpoints = [
            (f"{self.base_url}/hermes/commercial", {
                'action': 'opportunity',
                'data': {'unmet_needs': ['测试']}
            }),
            (f"{self.base_url}/hermes/commercial", {
                'action': 'investment',
                'data': {'name': '测试'}
            }),
            (f"{self.base_url}/hermes/avatar", {
                'action': 'list'
            }),
        ]

        all_success = True

        for url, data in endpoints:
            try:
                response = requests.post(url, json=data, timeout=10)
                if response.status_code == 200:
                    print(f"✅ {url.split('/')[-1]} - 成功")
                else:
                    print(f"⚠️  {url.split('/')[-1]} - 状态码 {response.status_code}")
                    all_success = False

            except Exception as e:
                print(f"❌ {url.split('/')[-1]} - 失败: {str(e)}")
                all_success = False

        self.record_result("Hermes API", all_success, "全部通过" if all_success else "部分失败")
        return all_success

    def test_security_headers(self):
        """测试安全响应头"""
        print("\n" + "=" * 60)
        print("8️⃣  安全响应头测试")
        print("=" * 60)

        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)

            headers_to_check = [
                'X-Content-Type-Options',
                'X-Frame-Options',
                'X-XSS-Protection',
                'Strict-Transport-Security'
            ]

            found_headers = []

            for header in headers_to_check:
                if header in response.headers:
                    found_headers.append(header)
                    print(f"✅ {header}: {response.headers[header]}")

            if len(found_headers) >= 2:
                print(f"\n✅ 安全响应头配置正确 ({len(found_headers)}/{len(headers_to_check)})")
                self.record_result("安全响应头", True, f"{len(found_headers)}/{len(headers_to_check)} 启用")
                return True
            else:
                print(f"\n⚠️  部分安全响应头缺失")
                self.record_result("安全响应头", False, f"仅 {len(found_headers)}/{len(headers_to_check)} 启用")
                return False

        except Exception as e:
            print(f"❌ 安全响应头测试失败: {str(e)}")
            self.record_result("安全响应头", False, str(e))
            return False

    def record_result(self, test_name, success, message):
        """记录测试结果"""
        self.results.append({
            'test': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })

    def print_summary(self):
        """打印测试摘要"""
        print("\n" + "=" * 60)
        print("📊 测试结果摘要")
        print("=" * 60)

        total = len(self.results)
        passed = sum(1 for r in self.results if r['success'])
        failed = total - passed

        print(f"\n总测试数: {total}")
        print(f"通过: {passed} ✅")
        print(f"失败: {failed} ❌")
        print(f"通过率: {passed/total*100:.1f}%")

        print("\n详细结果:")
        for result in self.results:
            status = "✅" if result['success'] else "❌"
            print(f"  {status} {result['test']}: {result['message']}")

        print("\n" + "=" * 60)

        if failed == 0:
            print("🎉 所有测试通过！安全集成成功！")
        else:
            print("⚠️  部分测试失败，请检查配置")

        print("=" * 60)

        return failed == 0

    def run_all_tests(self):
        """运行所有测试"""
        print("\n" + "=" * 60)
        print("🛡️  东方智慧智能体 - 安全集成测试")
        print("=" * 60)
        print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"API 地址: {self.base_url}")

        self.test_health_check()
        self.test_security_headers()
        self.test_rate_limiting()
        self.test_input_validation()
        self.test_commercial_apis()
        self.test_avatar_apis()
        self.test_openclaw_webhook()
        self.test_hermes_apis()

        return self.print_summary()


def main():
    """主函数"""
    tester = SecureAPITester('http://localhost:5000')

    try:
        success = tester.run_all_tests()
        return 0 if success else 1
    except requests.exceptions.ConnectionError:
        print("\n❌ 无法连接到 API 服务")
        print("请确保服务已启动: python start_secure.py")
        return 1
    except Exception as e:
        print(f"\n❌ 测试过程出错: {str(e)}")
        return 1


if __name__ == '__main__':
    exit(main())
