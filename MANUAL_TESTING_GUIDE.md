# 🧪 手动测试指南

## 快速测试

### 自动化测试
```bash
python3 simple_test.py
```

### 手动终端交互

1. **启动服务器**：
   ```bash
   python3 start_mcp_server.py
   ```

2. **在新终端中按顺序输入**：

   **初始化**：
   ```json
   {"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}
   ```

   **发送初始化完成**：
   ```json
   {"jsonrpc":"2.0","method":"notifications/initialized","params":{}}
   ```

   **更新任务状态**：
   ```json
   {"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"update_task_status","arguments":{"task_id":"task-001","agent_id":"test-agent","status":"running","current_action":"编写代码","message":"测试任务","progress_percentage":50}}}
   ```

   **获取任务状态**：
   ```json
   {"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_task_status","arguments":{"task_id":"task-001"}}}
   ```

   **获取 Agent 状态**：
   ```json
   {"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"get_agent_status","arguments":{"agent_id":"test-agent"}}}
   ```

## 可用工具

- `update_task_status` - 更新任务状态
- `get_task_status` - 获取任务状态  
- `get_agent_status` - 获取 Agent 状态
- `list_running_tasks` - 列出运行中的任务
- `get_storage_info` - 获取存储信息

## 状态说明

- **任务状态**: `running`, `success`, `failed`
- **存储路径**: `~/.task-manager/agent-status/` (可通过环境变量 `AGENT_STATUS_STORAGE_PATH` 配置)
- **数据关系**: 一个 Agent 可以执行多个 Task，但同时只能有一个活跃的 Task