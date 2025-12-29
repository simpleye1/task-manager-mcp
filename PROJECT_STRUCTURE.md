# Agent Status MCP 项目结构

## 📁 文件组织

```
agent-sync-mcp/
├── 🔧 核心文件
│   ├── agent_status_mcp.py          # MCP 服务器主实现
│   └── start_mcp_server.py          # 服务器启动脚本
│
├── 🧪 测试和示例
│   ├── test_agent_status_mcp.py     # 完整测试套件
│   └── example_claude_agent.py     # Claude Agent 使用示例
│
├── ⚙️ 配置文件
│   ├── requirements.txt            # Python 依赖
│   └── mcp-config-example.json     # MCP 配置模板
│
└── 📚 文档
    ├── README.md                   # 主要文档
    ├── AGENT_USAGE_GUIDE.md        # Agent 使用指南
    ├── PROJECT_SUMMARY.md          # 项目技术总结
    └── PROJECT_STRUCTURE.md        # 本文件
```

## 🔧 核心文件详解

### `agent_status_mcp.py` - 主实现文件
**功能**: MCP 服务器的完整实现
**包含**:
- 数据结构定义 (`TaskStatus`, `AgentAction`, `AgentStatus`)
- 本地文件存储类 (`LocalFileStorage`)
- 7个 MCP 工具函数
- FastMCP 服务器配置

**关键组件**:
```python
# 枚举定义
class TaskStatus(Enum): ...
class AgentAction(Enum): ...

# 数据结构
@dataclass
class AgentStatus: ...

# 存储管理
class LocalFileStorage: ...

# MCP 工具
@mcp.tool()
def initialize_agent_session(): ...
@mcp.tool() 
def update_agent_status(): ...
# ... 其他工具
```

### `start_mcp_server.py` - 启动脚本
**功能**: 提供友好的服务器启动界面
**特点**:
- 显示可用工具列表
- 显示存储路径信息
- 优雅的错误处理

## 🧪 测试和示例

### `test_agent_status_mcp.py` - 完整测试套件
**测试覆盖**:
1. **数据结构测试** - 验证枚举和数据类
2. **存储功能测试** - 验证文件读写操作
3. **状态转换测试** - 验证完整工作流程
4. **MCP 工具测试** - 模拟工具功能
5. **错误处理测试** - 验证异常情况
6. **边界情况测试** - 验证极端输入

**测试架构**:
```python
class TestSuite:
    def run_test(self, name, func): ...
    def cleanup(self): ...
    def print_summary(self): ...

# 6个独立测试函数
def test_data_structures(): ...
def test_local_storage(): ...
def test_status_transitions(): ...
def test_mcp_tools_simulation(): ...
def test_error_handling(): ...
def test_edge_cases(): ...
```

### `example_claude_agent.py` - 使用示例
**演示内容**:
- 智能会话初始化
- 枚举值验证
- 完整工作流程
- 错误处理机制

## ⚙️ 配置文件

### `requirements.txt`
```
fastmcp>=2.14.1
```

### `mcp-config-example.json`
Kiro MCP 配置模板，包含自动批准的工具列表。

## 📚 文档结构

### `README.md` - 主文档
- 项目概述和功能特性
- 安装和使用说明
- MCP 工具详细说明
- 数据结构文档

### `AGENT_USAGE_GUIDE.md` - 使用指南
- 解决枚举值问题的方案
- 推荐使用流程
- 错误处理指南
- 最佳实践

### `PROJECT_SUMMARY.md` - 技术总结
- 架构设计说明
- 扩展性分析
- 部署建议

## 🗂️ 运行时文件结构

服务器运行时会创建以下目录结构：

```
~/.task-manager/agent-sync-mcp/
├── agents/                    # Agent 状态文件
│   ├── claude-coder-001.json
│   └── claude-coder-002.json
├── tasks/                     # 任务状态文件
│   ├── task-20241229-001.json
│   └── task-20241229-002.json
└── logs/                      # 日志文件 (预留)
```

## 🚀 快速开始

1. **安装依赖**:
   ```bash
   pip install fastmcp
   ```

2. **运行测试**:
   ```bash
   python3 test_agent_status_mcp.py
   ```

3. **启动服务器**:
   ```bash
   python3 start_mcp_server.py
   ```

4. **查看示例**:
   ```bash
   python3 example_claude_agent.py
   ```

## 🔄 开发工作流

1. **修改核心逻辑** → 编辑 `agent_status_mcp.py`
2. **添加测试** → 更新 `test_agent_status_mcp.py`
3. **运行测试** → 验证功能正常
4. **更新文档** → 同步修改相关文档
5. **测试示例** → 确保示例代码正常运行

这个结构确保了代码的清晰性、可维护性和可扩展性。