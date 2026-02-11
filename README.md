# Task Manager MCP

Nova Agent 进度汇报 MCP 服务器。

## 安装

### 方式 1: Docker 安装（推荐）

#### 1. 构建 Docker 镜像

```bash
./build-docker.sh
```

#### 2. 添加到 Claude Desktop

**macOS/Windows:**

```bash
claude mcp add task-manager -s user \
  --env "TASK_MANAGER_HOST=host.docker.internal" \
  --env "TASK_MANAGER_PORT=8080" \
  --env "TASK_MANAGER_TIMEOUT=30" \
  --env "USE_MOCK_CLIENT=false" \
  -- docker run -i --rm \
    -e TASK_MANAGER_HOST \
    -e TASK_MANAGER_PORT \
    -e TASK_MANAGER_TIMEOUT \
    -e USE_MOCK_CLIENT \
    task-manager-mcp:latest
```

**Linux:**

```bash
claude mcp add task-manager -s user \
  --env "TASK_MANAGER_HOST=localhost" \
  --env "TASK_MANAGER_PORT=8080" \
  --env "TASK_MANAGER_TIMEOUT=30" \
  --env "USE_MOCK_CLIENT=false" \
  -- docker run -i --rm --network=host \
    -e TASK_MANAGER_HOST \
    -e TASK_MANAGER_PORT \
    -e TASK_MANAGER_TIMEOUT \
    -e USE_MOCK_CLIENT \
    task-manager-mcp:latest
```

**Mock 模式（测试用）:**

```bash
claude mcp add task-manager-mock -s user \
  --env "USE_MOCK_CLIENT=true" \
  -- docker run -i --rm \
    -e USE_MOCK_CLIENT \
    task-manager-mcp:latest
```

### 方式 2: 本地 Python 安装

#### 1. 安装依赖

```bash
pip install -r requirements.txt
```

#### 2. 手动配置 MCP

编辑 Claude Desktop 的 MCP 配置文件（参考 `mcp-config-example.json`）：

```json
{
  "mcpServers": {
    "task-manager": {
      "command": "python3",
      "args": ["/path/to/your/task_manager_mcp.py"],
      "env": {
        "TASK_MANAGER_HOST": "localhost",
        "TASK_MANAGER_PORT": "8080",
        "TASK_MANAGER_TIMEOUT": "30",
        "USE_MOCK_CLIENT": "false"
      }
    }
  }
}
```

### 卸载

```bash
# 删除 MCP 服务器
claude mcp remove task-manager

# 或删除 mock 版本
claude mcp remove task-manager-mock
```

## MCP Tools

| Tool | 用途 |
|------|------|
| `update_execution_session` | 更新 execution 的 session_id |
| `create_step` | 创建步骤，返回 step_id |
| `update_step` | 更新步骤状态/消息 |
| `health_check` | 健康检查 |

## 使用示例

```python
# 1. 注册 session
update_execution_session(execution_id="exec-123", session_id="nova-001")

# 2. 创建步骤
result = create_step(execution_id="exec-123", step_name="analyzing")
step_id = result["step_id"]

# 3. 完成步骤
update_step(execution_id="exec-123", step_id=step_id, status="completed")
```

## Step Status

- `running` - 执行中
- `completed` - 完成
- `failed` - 失败
- `skipped` - 跳过

## 配置

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `TASK_MANAGER_HOST` | Task Manager 服务地址 | `localhost` |
| `TASK_MANAGER_PORT` | Task Manager 服务端口 | `8080` |
| `TASK_MANAGER_TIMEOUT` | 请求超时时间（秒） | `30` |
| `USE_MOCK_CLIENT` | 是否使用 Mock 客户端 | `false` |

### Docker 网络说明

- **macOS/Windows**: 使用 `host.docker.internal` 访问宿主机服务
- **Linux**: 使用 `--network=host` 和 `localhost` 访问宿主机服务

## 开发

### 本地运行

```bash
pip install -r requirements.txt
python task_manager_mcp.py
```

### 运行测试

```bash
make test
# 或
python tests/simple_test.py
python tests/test_generated_client.py
```

## 错误处理

当后端 API 不可用时，MCP 会返回清晰的错误信息：

**404 错误（API 未实现）:**
```json
{
  "success": false,
  "error": "API endpoint not found: PATCH /api/executions/{id}/steps/{step_id}. The backend service may not have implemented this API yet.",
  "status_code": 404,
  "hint": "Please check if the Task Manager backend service has this endpoint implemented."
}
```

**连接失败:**
```json
{
  "success": false,
  "error": "Cannot connect to Task Manager service at http://localhost:8080",
  "hint": "Please verify that the Task Manager service is running and the host/port are correct."
}
```

## 配置

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `TASK_MANAGER_HOST` | Task Manager 服务地址 | `localhost` |
| `TASK_MANAGER_PORT` | Task Manager 服务端口 | `8080` |
| `TASK_MANAGER_TIMEOUT` | 请求超时时间（秒） | `30` |
| `USE_MOCK_CLIENT` | 是否使用 Mock 客户端 | `false` |

### Docker 网络说明

- **macOS/Windows**: 使用 `host.docker.internal` 访问宿主机服务
- **Linux**: 使用 `--network=host` 和 `localhost` 访问宿主机服务

## 开发

### 本地运行

```bash
pip install -r requirements.txt
python task_manager_mcp.py
```

### 运行测试

```bash
make test
# 或
python tests/simple_test.py
python tests/test_generated_client.py
```

## 错误处理

当后端 API 不可用时，MCP 会返回清晰的错误信息：

**404 错误（API 未实现）:**
```json
{
  "success": false,
  "error": "API endpoint not found: PATCH /api/executions/{id}/steps/{step_id}. The backend service may not have implemented this API yet.",
  "status_code": 404,
  "hint": "Please check if the Task Manager backend service has this endpoint implemented."
}
```

**连接失败:**
```json
{
  "success": false,
  "error": "Cannot connect to Task Manager service at http://localhost:8080",
  "hint": "Please verify that the Task Manager service is running and the host/port are correct."
}
```

## Step Status

- `running` - 执行中
- `completed` - 完成
- `failed` - 失败
- `skipped` - 跳过
