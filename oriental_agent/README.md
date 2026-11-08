# 东方智慧智能体

对话内核与 HTTP 服务各有一个入口。`oriental_agent.py` 已废弃，文件还在，但不要用它启动。

## 入口

| 用途 | 命令 |
|------|------|
| 对话内核 | `python -m core.agent` |
| HTTP 服务 | `python integration/api_server_secure.py` |
| 本地桌面脚本 | `./start_xiaoyuan.sh` 或 `start_xiaoyuan.bat` |

HTTP 进程加载的是 `core.agent.OrientalWisdomAgent`，路由在 `integration/api_server_secure.py`。

服务进程里只有一条 asyncio 循环：启动时调用一次 `agent.start()`，每个请求把 `process()` 交进去，不再对同一个智能体反复 `asyncio.run`。`DEBUG` 保持 `false`。默认监听 `127.0.0.1`；要给另一台机器用时再设置 `HOST`。

问候和置信度不足的句子不跑思考、身体和形象，也不写入记忆。商道和预测只处理主意图。没有年度现金流时，投资回复直接说明数据不足，不报一个算完的 ROI。

记忆默认最多 1000 条，检索只看权重和最近访问的前 200 条。衰减在一个事务里更新强度，不改写 `last_accessed`。SQLite 使用 WAL，写操作带 `busy_timeout`。同一句话的预测置信度由问句决定，重复询问结果相同。

易经转移计数和记忆写在同一个库里，路径仍是 `MEMORY_DB_PATH`。进程重新打开该库后，转移计数和概率与关闭前一致。

多 worker 可以共用这个库：每个进程单独打开连接，内存索引不是跨进程共享的，读之前若修订号变了就从数据库重读。事件循环和队列只在本进程内。不要用 `gunicorn --preload`，否则会把已经启动的循环和连接复进子进程。

## 安装

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

依赖：`pyyaml`、`flask`、`flask-cors`、`requests`、`pytest`。

## 配置

复制 `integration/.env.example` 为仓库根目录 `.env` 或 `integration/.env`。

生产姿态下 `DEBUG` 默认 `false`。启动前至少设置一项认证，字段与 `integration/config_secure.py` 对齐：

- `API_KEYS`（或 `API_KEY`）→ `api_keys.keys`，请求头 `X-API-Key`
- `API_AUTH_TOKEN`（或 `BEARER_TOKEN`）→ `bearer_auth.token`，请求头 `Authorization: Bearer <token>`

两项都空时，服务拒绝启动；除 `GET /health` 外，请求返回 401。

```bash
export API_AUTH_TOKEN=change-me
export DEBUG=false
python integration/api_server_secure.py
```

对话示例：

```bash
curl -X POST http://127.0.0.1:5000/api/dialog \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $API_AUTH_TOKEN" \
  -d '{"message": "我想投资10万", "user_id": "local"}'
```

## 测试

```bash
python -m compileall -q .
python -m pytest
```

`tests/` 覆盖投资 ROI / NPV / IRR、意图路由，以及中文「投资10万」不再因缺少 `initial_investment` 而 `KeyError`。没有「823 个测试全部通过」这套用例，文档里也不再这么写。

`verify_system.py` 和 `verify_system_v2.py` 用正常 import 做手工核对，不是验收套件。

## 预测与商机

预测引擎默认在结果里附上启发式免责声明。设置 `PREDICTION_HEURISTIC_DISCLAIMER=false` 才关闭。

商机洞察不再用随机数填收入。没有市场信号或没有收入数字时，返回「数据不足」。

## P2

### 五行和八识

约定在 `core/metaphor_invariants.py`，并接到现有路径上：

- 五行：当前旺的一行按 `memory/wuxing.py` 的生克表改变记忆强度衰减。相生更慢，相克更快，其余中性。对话进程里的衰减循环调用 `MemorySystem.apply_wuxing_decay_step`。
- 八识：激活度按固定表加到意图置信度上，结果夹在 0 到 1。激活度为 0 时不改已有意图，也不给「投资」加分。`OrientalWisdomAgent.process` 在识别意图之后使用这张表。

`tests/test_metaphor_invariants.py` 锁住这些关系。

### 记忆持久化

`MemorySystem` 不传 `persist_path` 时仍只在内存中。对话内核默认把这一条路径写到 `data/agent_memory.sqlite`，包括干支标签和记忆关联。设置 `MEMORY_DB_PATH` 可改位置；设成空字符串则退回纯内存。已有的旧库会自动补列。冒烟测试在 `tests/test_memory_persistence.py`，覆盖换实例检索，以及对话 `process` 写入后重新打开仍能按关键词找回。

空闲衰减仍按五行倍率（相生 0.5、中性 1、相克 1.5）。默认步长是 `memory.wuxing_decay_rate=0.001`，避免每分钟按 0.05 把强度打掉。不变量测试里的参考步长仍是 0.05。

### 双源

`oriental_agent.py` 继续标为 DEPRECATED，文件保留，但是禁止再被运行时代码导入。

- 禁止 `import oriental_agent` 或 `from oriental_agent import ...`。内核、HTTP、测试和脚本都不要新增这种引用。
- 禁止把它和 `core/`、`memory/` 等包互相同步。行为以包内实现为准。
- 允许只把它当历史对照读。

### 武学叙事和安全

太极、易筋经、五禽戏是叙事状态机，代码在 `narrative/martial_state_machine.py`。`security/martial_defense.py` 只是兼容垫片，不是访问控制。

认证、限流和安全响应头只在 `integration/config_secure.py` 与 `integration/api_server_secure.py`。

### CI

`.github/workflows/ci.yml` 调用 `scripts/ci.sh`：`compileall`、`pytest`，以及 `scripts/health_check.py`（`/health` 返回 200，未带凭据的 `/api/dialog` 返回 401）。本地也可以直接跑：

```bash
bash scripts/ci.sh
```
