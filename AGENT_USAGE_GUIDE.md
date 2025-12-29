# Claude Agent 使用指南

## 问题解答：Agent 如何知道可用的枚举值？

在实际的 MCP 交互中，Claude agent 默认**不会自动知道**你定义的枚举值。为了解决这个问题，我们提供了以下解决方案：

## 解决方案

### 1. 初始化会话工具 (推荐)

在开始使用状态跟踪之前，Claude agent 应该首先调用 `initialize_agent_session` 工具：

```python
# Agent 首次使用时调用
result = await initialize_agent_session(agent_id="claude-coder-001")

# 返回的数据包含：
{
  "success": true,
  "data": {
    "agent_id": "claude-coder-001",
    "available_options": {
      "task_statuses": {
        "pending": "等待执行 - 任务已创建但尚未开始",
        "running": "正在执行 - 任务正在进行中",
        "completed": "已完成 - 任务成功完成",
        "failed": "执行失败 - 任务执行过程中出现错误",
        "cancelled": "已取消 - 任务被手动取消"
      },
      "agent_actions": {
        "code_analysis": "代码分析 - 分析现有代码结构",
        "code_writing": "代码编写 - 编写新的代码功能",
        "code_review": "代码审查 - 审查代码质量",
        "testing": "测试执行 - 运行测试套件",
        "pr_creation": "创建 Pull Request - 创建代码合并请求",
        "pr_update": "更新 Pull Request - 更新现有的合并请求",
        "error_handling": "错误处理 - 处理执行过程中的错误",
        "waiting_input": "等待输入 - 等待用户或系统输入"
      }
    },
    "usage_guide": {
      "example": {
        "agent_id": "claude-coder-001",
        "task_id": "task-example-001",
        "status": "running",
        "current_action": "code_writing",
        "progress_percentage": 50,
        "message": "正在编写用户认证功能"
      }
    }
  }
}
```

### 2. 获取可用状态工具

如果只需要快速查看可用的枚举值，可以调用 `get_available_statuses`：

```python
result = await get_available_statuses()

# 返回简化的枚举列表：
{
  "success": true,
  "data": {
    "task_statuses": ["pending", "running", "completed", "failed", "cancelled"],
    "agent_actions": ["code_analysis", "code_writing", "code_review", "testing", "pr_creation", "pr_update", "error_handling", "waiting_input"]
  }
}
```

### 3. 改进的工具文档

`update_agent_status` 工具的文档字符串现在明确列出了所有可用值：

```python
def update_agent_status(
    agent_id: str,
    task_id: str,
    status: str,  # 可选值: pending, running, completed, failed, cancelled
    message: str,
    current_action: Optional[str] = None,  # 可选值: code_analysis, code_writing, code_review, testing, pr_creation, pr_update, error_handling, waiting_input
    progress_percentage: float = 0.0,
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
```

## 推荐的使用流程

### 步骤 1: 初始化会话
```python
# Claude agent 开始工作时
session_info = await initialize_agent_session("claude-coder-001")
available_statuses = session_info["data"]["available_options"]["task_statuses"]
available_actions = session_info["data"]["available_options"]["agent_actions"]
```

### 步骤 2: 使用正确的枚举值
```python
# 开始任务
await update_agent_status(
    agent_id="claude-coder-001",
    task_id="task-20241229-001",
    status="running",  # 从 available_statuses 中选择
    current_action="code_analysis",  # 从 available_actions 中选择
    progress_percentage=10,
    message="开始分析代码结构"
)

# 更新进度
await update_agent_status(
    agent_id="claude-coder-001",
    task_id="task-20241229-001", 
    status="running",
    current_action="code_writing",
    progress_percentage=50,
    message="正在编写新功能"
)

# 完成任务
await update_agent_status(
    agent_id="claude-coder-001",
    task_id="task-20241229-001",
    status="completed",
    current_action=None,
    progress_percentage=100,
    message="任务完成"
)
```

## 可用的状态和动作

### 任务状态 (status)
- `pending`: 等待执行
- `running`: 正在执行
- `completed`: 已完成
- `failed`: 执行失败
- `cancelled`: 已取消

### Agent 动作 (current_action)
- `code_analysis`: 代码分析
- `code_writing`: 代码编写
- `code_review`: 代码审查
- `testing`: 测试执行
- `pr_creation`: 创建 Pull Request
- `pr_update`: 更新 Pull Request
- `error_handling`: 错误处理
- `waiting_input`: 等待输入

## 错误处理

如果使用了无效的枚举值，系统会返回错误：

```python
# 错误示例
result = await update_agent_status(
    agent_id="claude-coder-001",
    task_id="task-001",
    status="invalid_status",  # 无效状态
    message="测试"
)

# 返回错误
{
  "success": false,
  "error": "无效的状态值: 'invalid_status' is not a valid TaskStatus"
}
```

## 最佳实践

1. **总是先初始化**: 在使用状态跟踪之前调用 `initialize_agent_session`
2. **使用正确的值**: 只使用返回的可用枚举值
3. **提供有意义的消息**: message 字段应该描述当前正在做什么
4. **合理的进度更新**: progress_percentage 应该反映真实进度
5. **丰富的详情信息**: 在 details 中提供额外的上下文信息

这样，Claude agent 就能够正确地使用所有可用的状态和动作类型了！