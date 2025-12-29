# Agent Status MCP Server

一个用于跟踪 Claude agent 执行状态的 MCP (Model Context Protocol) 服务器。

## 功能特性

- 📊 实时跟踪 agent 执行状态
- 📝 记录详细的任务进度和操作历史
- 💾 本地文件存储（支持后续扩展到数据库）
- 🔍 查询 agent 和任务状态
- 📈 进度百分比跟踪
- 🏷️ 丰富的状态分类和动作类型

## 数据结构设计

### 任务状态 (TaskStatus)
- `PENDING`: 等待执行
- `RUNNING`: 正在执行
- `COMPLETED`: 已完成
- `FAILED`: 执行失败
- `CANCELLED`: 已取消

### Agent 动作类型 (AgentAction)
- `CODE_ANALYSIS`: 代码分析
- `CODE_WRITING`: 代码编写
- `CODE_REVIEW`: 代码审查
- `TESTING`: 测试执行
- `PR_CREATION`: 创建 Pull Request
- `PR_UPDATE`: 更新 Pull Request
- `ERROR_HANDLING`: 错误处理
- `WAITING_INPUT`: 等待输入

### 状态数据结构
```python
@dataclass
class AgentStatus:
    agent_id: str              # Agent 唯一标识
    task_id: str               # 任务唯一标识
    status: TaskStatus         # 任务状态
    current_action: AgentAction # 当前动作
    progress_percentage: float  # 进度百分比 (0-100)
    message: str               # 状态描述
    details: Dict[str, Any]    # 额外详情
    timestamp: str             # 时间戳
```

## 安装和使用

### 1. 安装依赖
```bash
pip install fastmcp
```

### 2. 运行 MCP 服务器
```bash
python agent_status_mcp.py
```

### 3. 配置 MCP 客户端
在你的 MCP 配置文件中添加：
```json
{
  "mcpServers": {
    "agent-status": {
      "command": "python",
      "args": ["/path/to/agent_status_mcp.py"],
      "env": {}
    }
  }
}
```

## 重要：Claude Agent 如何知道可用的枚举值？

在实际的 MCP 交互中，Claude agent 默认**不会自动知道**你定义的枚举值。为了解决这个问题：

### 解决方案 1: 初始化会话 (推荐)
```python
# Agent 首次使用时调用
session_info = await initialize_agent_session("claude-coder-001")
# 返回所有可用的状态和动作类型，以及使用示例
```

### 解决方案 2: 查询可用状态
```python
# 快速获取枚举值列表
statuses = await get_available_statuses()
```

### 解决方案 3: 查看工具文档
`update_agent_status` 工具的文档字符串现在明确列出了所有可用值。

详细使用指南请参考 [AGENT_USAGE_GUIDE.md](AGENT_USAGE_GUIDE.md)

## MCP 工具 (Tools)

### 0. initialize_agent_session (推荐首先调用)
初始化 agent 会话，获取所有可用的状态和动作类型
```python
initialize_agent_session(agent_id="claude-coder-001")
```
**重要**: Claude agent 在开始使用前应该先调用此工具来了解可用的枚举值。

### 1. update_agent_status
更新 agent 状态
```python
update_agent_status(
    agent_id="claude-coder-001",
    task_id="task-20241229-143022",
    status="running",
    message="正在分析代码结构",
    current_action="code_analysis",
    progress_percentage=25.0,
    details={
        "files_analyzed": 5,
        "complexity": "medium"
    }
)
```

### 2. get_available_statuses
获取所有可用的状态和动作枚举值
```python
get_available_statuses()
```

### 3. update_agent_status
获取 agent 当前状态和历史
```python
get_agent_status(agent_id="claude-coder-001")
```

### 4. get_agent_status
获取 agent 当前状态和历史
```python
get_agent_status(agent_id="claude-coder-001")
```

### 5. get_task_status
获取任务状态
```python
get_task_status(task_id="task-20241229-143022")
```

### 6. list_active_agents
列出所有活跃的 agents
```python
list_active_agents()
```

### 7. get_storage_info
获取存储信息和统计
```python
get_storage_info()
```

## 存储结构

默认存储路径：`~/.task-manager/agent-sync-mcp/`

```
~/.task-manager/agent-sync-mcp/
├── agents/          # Agent 状态文件
│   ├── claude-coder-001.json
│   └── claude-coder-002.json
├── tasks/           # 任务状态文件
│   ├── task-20241229-143022.json
│   └── task-20241229-143045.json
└── logs/            # 日志文件 (预留)
```

### Agent 文件格式
```json
{
  "agent_id": "claude-coder-001",
  "current_status": {
    "agent_id": "claude-coder-001",
    "task_id": "task-20241229-143022",
    "status": "running",
    "current_action": "code_writing",
    "progress_percentage": 60.0,
    "message": "正在编写新功能代码",
    "details": {
      "files_modified": ["src/main.py"],
      "lines_added": 45
    },
    "timestamp": "2024-12-29T14:30:22Z"
  },
  "last_updated": "2024-12-29T14:30:22Z",
  "history": [
    // 最近100条状态历史
  ]
}
```

## 使用示例

查看 `example_usage.py` 文件，了解如何在 Claude agent 中集成状态跟踪。

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
        "update_agent_status",
        "get_agent_status", 
        "list_active_agents"
      ]
    }
  }
}
```

### 4. 在 Claude Agent 中使用
```python
# 在你的 Claude Agent 代码中
await update_agent_status(
    agent_id="claude-coder-001",
    task_id="task-20241229-143022", 
    status="running",
    current_action="code_writing",
    progress_percentage=60,
    message="正在编写新功能代码",
    details={
        "files_modified": ["src/main.py"],
        "lines_added": 45
    }
)
```

## 项目文件说明

| 文件 | 说明 |
|------|------|
| `agent_status_mcp.py` | **核心文件** - MCP 服务器实现，包含所有数据结构、存储逻辑和工具 |
| `start_mcp_server.py` | **启动脚本** - 友好的服务器启动界面 |
| `test_agent_status_mcp.py` | **完整测试套件** - 包含所有功能测试 |
| `example_claude_agent.py` | **使用示例** - 展示 Claude Agent 如何正确使用 MCP |
| `requirements.txt` | **依赖文件** - Python 包依赖列表 |
| `mcp-config-example.json` | **配置示例** - Kiro MCP 配置模板 |
| `README.md` | **项目文档** - 完整的使用说明 |
| `AGENT_USAGE_GUIDE.md` | **使用指南** - Claude Agent 集成指南 |
| `PROJECT_SUMMARY.md` | **项目总结** - 技术架构和设计说明 |

## 测试

运行完整测试套件：
```bash
python3 test_agent_status_mcp.py
```

运行使用示例：
```bash
python3 example_claude_agent.py
```

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