# 东方智慧智能体本地集成测试指南

## 📋 测试前准备

### 1. 确认环境

```bash
# 确认 Python 版本
python3 --version  # 需要 >= 3.8

# 确认 OpenClaw 已安装
openclaw --version

# 确认 Hermes Agent 已安装
hermes --version
```

### 2. 安装依赖

```bash
cd oriental_agent

# 安装 Python 依赖
pip install pyyaml flask flask-cors requests

# (可选) 安装 gunicorn 用于生产环境
pip install gunicorn
```

---

## 🚀 本地测试步骤

### 第一步：启动东方智慧智能体 API

```bash
# 终端 1 - 启动 API 服务
cd oriental_agent
python integration/api_server.py
```

应该看到：
```
============================================================
🧘 东方智慧智能体 API 服务
============================================================
📍 本地地址: http://localhost:5000
📍 OpenClaw Webhook: http://localhost:5000/webhook/openclaw
📍 Hermes接口: http://localhost:5000/hermes/commercial
============================================================
```

### 第二步：运行集成测试

```bash
# 终端 2 - 运行测试
cd oriental_agent
python integration/test_integration.py
```

### 第三步：配置 OpenClaw

```bash
# 复制配置文件
cp integration/openclaw_config.json ~/.openclaw/config.json

# 编辑配置文件，填入你的 Bot Token
nano ~/.openclaw/config.json

# 重启 OpenClaw
openclaw restart
```

### 第四步：配置 Hermes Agent

```bash
# 复制配置文件
cp integration/hermes_config.yaml ~/.hermes/config.yaml

# 编辑配置文件
nano ~/.hermes/config.yaml

# 重启 Hermes
hermes restart
```

---

## 📊 测试验证清单

### ✅ API 服务测试

```bash
# 测试 API 是否正常
curl http://localhost:5000/health

# 预期输出：
# {"status": "ok", "service": "Oriental Wisdom Agent", ...}
```

### ✅ 商道功能测试

```bash
# 测试商机分析
curl -X POST http://localhost:5000/api/commercial/opportunity \
  -H "Content-Type: application/json" \
  -d '{"unmet_needs": ["智能家居"], "technology_trends": ["AI"]}'

# 测试投资分析
curl -X POST http://localhost:5000/api/commercial/investment \
  -H "Content-Type: application/json" \
  -d '{"name": "测试项目", "initial_investment": 1000000, "annual_cash_flows": [300000, 400000, 500000]}'
```

### ✅ 形象系统测试

```bash
# 获取预设
curl http://localhost:5000/api/avatar/presets

# 创建形象
curl -X POST http://localhost:5000/api/avatar/create \
  -H "Content-Type: application/json" \
  -d '{"preset_id": "model_a", "name": "我的形象"}'
```

### ✅ OpenClaw 测试

```bash
# 发送测试消息
openclaw send "分析AI商机"

# 预期：收到商道分析回复
```

### ✅ Hermes Agent 测试

```bash
# 在 Hermes 中测试
/hermes analyze 投资分析 100万
```

---

## 🔧 常见问题

### Q1: API 启动失败，端口被占用

```bash
# 查看占用端口的进程
lsof -i :5000

# 杀死进程或使用其他端口
python integration/api_server.py --port 5001
```

### Q2: OpenClaw 无法连接

```bash
# 检查 OpenClaw 配置
cat ~/.openclaw/config.json

# 确保 webhook URL 正确
# 应为: http://localhost:5000/webhook/openclaw
```

### Q3: Hermes 无法调用商道功能

```bash
# 检查环境变量
echo $ORIENTAL_AGENT_URL

# 如果为空，设置它
export ORIENTAL_AGENT_URL=http://localhost:5000
```

### Q4: 测试脚本报错 "API服务未启动"

```bash
# 确保 API 服务正在运行
ps aux | grep api_server

# 如果没有，重新启动
python integration/api_server.py &
```

---

## 📁 集成文件说明

```
integration/
├── api_server.py              # API 服务主文件
├── test_integration.py        # 集成测试脚本
├── openclaw_config.json       # OpenClaw 配置
├── hermes_config.yaml         # Hermes 配置
├── hermes_skill_oriental.py  # Hermes 技能
├── openclaw_skill_oriental.py # OpenClaw 技能
└── .env.example               # 环境变量示例
```

---

## 🎯 成功标志

当以下测试全部通过时，说明集成成功：

- [ ] API 健康检查通过
- [ ] 商道分析返回结果
- [ ] 形象系统生成 SVG
- [ ] OpenClaw 收到回复
- [ ] Hermes 调用商道技能

---

## 📞 调试技巧

### 查看 API 日志

API 服务启动后会显示详细的请求日志。

### 查看 OpenClaw 日志

```bash
openclaw logs
```

### 查看 Hermes 日志

```bash
hermes logs
```

### 使用 curl 调试

```bash
# 详细显示请求和响应
curl -v http://localhost:5000/health

# 显示响应头
curl -I http://localhost:5000/health
```

---

## 下一步

本地测试通过后，可以部署到阿里云服务器：

1. 将代码上传到服务器
2. 使用 systemd 管理服务
3. 配置域名和 HTTPS
4. 启动生产环境服务
