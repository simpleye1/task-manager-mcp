# Agent Status MCP Server

一个用于跟踪 Claude agent 执行状态的 MCP (Model Context Protocol) 服务器。

## 功能特性

- 📊 实时跟踪 agent 执行状态
- 📝 记录任务进度和状态
- 💾 本地文件存储（支持后续扩展到数据库）
- 🔍 查询 agent 和任务状态
- 📈 进度百分比跟踪

## 数据模型

### 任务状态 (TaskStatus)
- `running`: 正在执行
- `success`: 执行成功
- `failed`: 执行失败

### 数据关系
- **Agent**: 执行任务的智能体（如 claude-coder-001）
- **Task**: Agent 执行的具体任务（如编写某个功能）
- 一个 Agent 可以执行多个 Task，但同时只能有一个活跃的 Task

### 数据结构
```python
@dataclass
class TaskInfo:
    task_id: str               # 任务唯一标识
    agent_id: str              # Agent 唯一标识
    status: TaskStatus         # 任务状态
    current_action: str        # 当前动作描述 (Agent 自定义)
    progress_percentage: float # 进度百分比 (0-100)
    message: str               # 状态描述
    details: Dict[str, Any]    # 额外详情
    created_at: str            # 创建时间
    updated_at: str            # 更新时间
```

## 快速开始

### 1. 安装依赖
```bash
pip install fastmcp
```

### 2. 启动 MCP 服务器
```bash
python3 start_mcp_server.py
```

### 3. 在 Kiro 中配置 MCP
将以下配置添加到你的 MCP 配置文件中：
```json
{
  "mcpServers": {
    "agent-status": {
      "command": "python3",
      "args": ["/path/to/your/start_mcp_server.py"],
      "disabled": false,
      "autoApprove": [
        "update_task_status",
        "get_task_status",
        "get_agent_status",
        "list_running_tasks",
        "get_storage_info"
      ]
    }
  }
}
```

### 4. 在 Claude Agent 中使用
```python
# 在你的 Claude Agent 代码中
await update_task_status(
    task_id="task-001",
    agent_id="claude-coder-001", 
    status="running",
    current_action="编写代码",
    message="正在编写新功能代码",
    progress_percentage=60,
    details={
        "files_modified": ["src/main.py"],
        "lines_added": 45
    }
)
```

## MCP 工具

### 1. update_task_status
更新任务状态
```python
update_task_status(
    task_id="task-001",
    agent_id="claude-coder-001",
    status="running",
    current_action="编写代码",
    message="正在编写新功能",
    progress_percentage=60.0,
    details={
        "files_modified": ["src/main.py"],
        "lines_added": 45
    }
)
```

### 2. get_task_status
获取任务状态
```python
get_task_status(task_id="task-001")
```

### 3. get_agent_status
获取 Agent 当前状态
```python
get_agent_status(agent_id="claude-coder-001")
```

### 4. list_running_tasks
列出所有运行中的任务
```python
list_running_tasks()
```

### 5. get_storage_info
获取存储信息和统计
```python
get_storage_info()
```

## 存储结构

默认存储路径：`~/.task-manager/agent-status/`

可通过环境变量 `AGENT_STATUS_STORAGE_PATH` 配置存储路径：
```bash
export AGENT_STATUS_STORAGE_PATH="/custom/path/to/storage"
python3 start_mcp_server.py
```

```
~/.task-manager/agent-status/
├── tasks/           # 任务状态文件
│   ├── task-001.json
│   └── task-002.json
└── agents/          # Agent 当前任务文件
    ├── claude-coder-001.json
    └── claude-coder-002.json
```

### 任务文件格式
```json
{
  "task_id": "task-001",
  "agent_id": "claude-coder-001",
  "status": "running",
  "current_action": "编写代码",
  "progress_percentage": 60.0,
  "message": "正在编写新功能代码",
  "details": {
    "files_modified": ["src/main.py"],
    "lines_added": 45
  },
  "created_at": "2024-12-29T14:30:22Z",
  "updated_at": "2024-12-29T14:35:22Z"
}
```

### Agent 文件格式
```json
{
  "agent_id": "claude-coder-001",
  "current_task": {
    // 当前任务的完整信息
  },
  "last_updated": "2024-12-29T14:35:22Z"
}
```

## 项目文件说明

| 文件 | 说明 |
|------|------|
| `agent_status_mcp.py` | **核心文件** - MCP 服务器实现，包含所有数据结构、存储逻辑和工具 |
| `start_mcp_server.py` | **启动脚本** - 友好的服务器启动界面 |
| `simple_test.py` | **简单测试** - 直接调用功能的测试脚本 |
| `requirements.txt` | **依赖文件** - Python 包依赖列表 |
| `mcp-config-example.json` | **配置示例** - Kiro MCP 配置模板 |
| `README.md` | **项目文档** - 完整的使用说明 |
| `MANUAL_TESTING_GUIDE.md` | **手动测试指南** - 终端 JSON-RPC 交互详细说明 |

## 测试

### 自动化测试
运行简单测试：
```bash
python3 simple_test.py
```

### 手动终端测试
详细的手动测试指南请参考：[MANUAL_TESTING_GUIDE.md](MANUAL_TESTING_GUIDE.md)

## 扩展计划

- [ ] 数据库存储支持 (PostgreSQL, SQLite)
- [ ] Web 界面监控面板
- [ ] 状态变更通知 (Webhook, Email)
- [ ] 性能指标统计
- [ ] 多 agent 协作状态跟踪
- [ ] 状态查询 API
- [ ] 实时状态推送 (WebSocket)

## 许可证

MIT License