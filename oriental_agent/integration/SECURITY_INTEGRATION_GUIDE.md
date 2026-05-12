# 东方智慧智能体 - 安全集成指南

## 📋 概述

本指南说明如何在**不修改 OpenClaw 和 Hermes 现有配置**的前提下，安全地集成东方智慧智能体。

### 核心原则

- ✅ **零配置修改** - 不改变 OpenClaw 和 Hermes 的配置文件
- ✅ **本地优先** - 智能体 API 仅在 localhost 运行
- ✅ **安全防护** - 多层安全机制保护系统
- ✅ **即插即用** - 保持现有配置，通过 webhook 和 API 接口集成

---

## 🔒 安全特性

### 1. 网络安全

| 特性 | 默认状态 | 说明 |
|------|---------|------|
| **IP 白名单** | ✅ 启用 | 仅允许本地访问 (127.0.0.1) |
| **绑定地址** | 127.0.0.1 | 仅监听本地回环接口 |
| **CORS** | ✅ 启用 | 限制跨域请求 |
| **请求大小限制** | 1 MB | 防止大文件攻击 |

### 2. 请求保护

| 特性 | 默认状态 | 说明 |
|------|---------|------|
| **频率限制** | ✅ 启用 | 60请求/分钟，1000请求/小时 |
| **输入验证** | ✅ 启用 | 验证和清洗所有输入数据 |
| **XSS 防护** | ✅ 启用 | 移除危险字符 |
| **请求日志** | ✅ 启用 | 记录所有访问日志 |

### 3. 响应安全

| 特性 | 默认状态 | 说明 |
|------|---------|------|
| **安全响应头** | ✅ 启用 | X-Frame-Options, X-Content-Type-Options 等 |
| **错误处理** | ✅ 启用 | 统一错误响应格式 |
| **异常捕获** | ✅ 启用 | 防止信息泄露 |

---

## 🚀 快速启动

### 方式一：使用启动脚本（推荐）

```bash
cd oriental_agent/integration

# 启动安全 API 服务
python start_secure.py
```

服务启动后会自动：
- 检查端口 5000 是否可用
- 启动 Flask API 服务
- 验证服务健康状态
- 显示连接信息

### 方式二：直接运行

```bash
cd oriental_agent/integration

# 启动 API 服务
python api_server_secure.py
```

---

## 🧪 测试集成

### 运行安全集成测试

```bash
cd oriental_agent/integration

# 测试安全特性
python test_secure_integration.py
```

测试内容：
1. ✅ 健康检查
2. ✅ 安全响应头
3. ✅ 频率限制
4. ✅ 输入验证
5. ✅ 商道 API
6. ✅ 形象 API
7. ✅ OpenClaw Webhook
8. ✅ Hermes API

---

## 🔧 配置说明

### 安全配置文件

编辑 `config_secure.py` 自定义安全设置：

```python
SECURITY_CONFIG = {
    'server': {
        'host': '127.0.0.1',  # 绑定地址
        'port': 5000,          # 端口
        'debug': True,
    },

    'rate_limiting': {
        'enabled': True,
        'requests_per_minute': 60,   # 每分钟限制
        'requests_per_hour': 1000,    # 每小时限制
    },

    'ip_whitelist': {
        'enabled': True,
        'allowed_ips': ['127.0.0.1', '::1', 'localhost'],
    },

    'input_validation': {
        'enabled': True,
        'max_text_length': 10000,
        'max_list_length': 1000,
    },
}
```

### 调整频率限制

如果需要更高的限制：

```python
'rate_limiting': {
    'enabled': True,
    'requests_per_minute': 120,  # 增加限制
    'requests_per_hour': 5000,
},
```

### 添加信任的 IP

如果需要从其他机器访问：

```python
'ip_whitelist': {
    'enabled': True,
    'allowed_ips': [
        '127.0.0.1',
        '::1',
        'localhost',
        '192.168.1.100',  # 添加信任的 IP
    ],
},
```

---

## 📡 API 接口

### OpenClaw Webhook

**地址**: `http://localhost:5000/webhook/openclaw`

OpenClaw 会自动将消息发送到此处，无需修改配置。

### Hermes Agent 接口

**地址**:
- 商道: `http://localhost:5000/hermes/commercial`
- 形象: `http://localhost:5000/hermes/avatar`

Hermes 通过这些接口调用智能体功能。

### 其他 API

| 端点 | 方法 | 说明 |
|------|------|------|
| `/health` | GET | 健康检查 |
| `/api/commercial/opportunity` | POST | 商机分析 |
| `/api/commercial/investment` | POST | 投资分析 |
| `/api/commercial/strategy` | POST | 战略规划 |
| `/api/avatar/create` | POST | 创建形象 |
| `/api/avatar/render` | GET | 渲染形象 |

---

## 🛡️ 安全机制详解

### 1. 请求前检查

```python
@app.before_request
def before_request_checks():
    # 检查请求大小
    if request.content_length > MAX_SIZE:
        return error_response()

    # 检查 IP 白名单
    if IP_WHITELIST_ENABLED:
        if request.remote_addr not in ALLOWED_IPS:
            return error_response()

    # 检查频率限制
    if not check_rate_limit(request.remote_addr):
        return error_response()
```

### 2. 输入验证和清洗

```python
def validate_input(data):
    # 验证文本长度
    if isinstance(data, str):
        if len(data) > MAX_LENGTH:
            return False, data[:MAX_LENGTH]

    # 递归验证字典和列表
    if isinstance(data, dict):
        return {k: validate_input(v) for k, v in data.items()}

    # 移除危险字符
    return data.replace('<', '').replace('>', '')
```

### 3. 安全响应头

```python
response.headers['X-Frame-Options'] = 'DENY'
response.headers['X-Content-Type-Options'] = 'nosniff'
response.headers['X-XSS-Protection'] = '1; mode=block'
response.headers['Strict-Transport-Security'] = 'max-age=31536000'
```

### 4. 异常处理

```python
@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled exception: {str(e)}")
    # 不暴露内部错误信息
    return jsonify({'error': 'An unexpected error occurred'}), 500
```

---

## 📊 监控和日志

### 查看日志

服务启动后会输出详细日志：

```bash
python start_secure.py
```

日志包含：
- 请求来源 IP
- 请求方法和路径
- 响应状态码
- 安全警告（如频率限制触发）
- 错误信息

### 日志分析

常见日志信息：

```
INFO: 127.0.0.1 - GET /health - Mozilla/5.0...
WARNING: Rate limit exceeded for IP 127.0.0.1 (per minute)
WARNING: Unauthorized IP access attempt: 192.168.1.100
ERROR: Server error: [具体错误]
```

---

## 🔍 故障排除

### 1. 端口被占用

```bash
# 检查端口占用
lsof -i :5000

# 停止占用进程或修改端口
```

### 2. IP 被拒绝访问

检查 `config_secure.py` 中的 `allowed_ips` 配置。

### 3. 频率限制触发

等待一分钟或调整 `requests_per_minute` 值。

### 4. 无法连接

确保服务正在运行：
```bash
ps aux | grep api_server_secure
```

---

## 🚀 生产环境部署

### 使用 systemd 管理服务

创建服务文件 `/etc/systemd/system/oriental-agent.service`:

```ini
[Unit]
Description=Oriental Wisdom Agent API Service
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/oriental_agent/integration
ExecStart=/usr/bin/python3 api_server_secure.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl enable oriental-agent
sudo systemctl start oriental-agent
sudo systemctl status oriental-agent
```

### 使用 gunicorn

```bash
pip install gunicorn

# 启动
gunicorn -w 4 -b 127.0.0.1:5000 api_server_secure:app
```

---

## ✅ 检查清单

在部署前，确认以下项目：

- [ ] 安全配置已检查
- [ ] 端口 5000 可用
- [ ] 防火墙允许本地访问
- [ ] 日志目录存在
- [ ] 依赖已安装
- [ ] OpenClaw 和 Hermes 配置未修改
- [ ] 测试通过
- [ ] 监控已配置

---

## 📞 支持

如遇问题：
1. 检查日志输出
2. 运行测试脚本验证
3. 确认网络和端口配置
4. 查看故障排除章节

---

## 🔄 更新和升级

### 升级智能体

```bash
# 停止服务
pkill -f api_server_secure

# 更新代码
git pull

# 重新启动
python start_secure.py
```

### 配置文件更新

保留 `config_secure.py` 的备份，更新时合并更改。

---

## 📚 相关文件

| 文件 | 用途 |
|------|------|
| `api_server_secure.py` | 安全 API 服务器主文件 |
| `config_secure.py` | 安全配置文件 |
| `start_secure.py` | 启动脚本 |
| `test_secure_integration.py` | 安全集成测试 |

---

## 🎯 总结

此安全集成方案：

✅ **不修改 OpenClaw 配置** - 使用现有 webhook 接口
✅ **不修改 Hermes 配置** - 使用现有 API 接口
✅ **本地安全运行** - 仅监听 localhost
✅ **多层安全防护** - IP白名单、频率限制、输入验证
✅ **完整监控日志** - 详细记录所有请求
✅ **即插即用** - 保持现有配置，快速集成

现在您可以在不影响现有 OpenClaw 和 Hermes 配置的情况下，安全地使用东方智慧智能体！
