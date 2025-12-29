#!/usr/bin/env python3
"""
启动 Agent Status MCP 服务器的脚本
"""

import sys
import os
from pathlib import Path

# 添加当前目录到 Python 路径
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# 导入并运行 MCP 服务器
from agent_status_mcp import mcp

if __name__ == "__main__":
    print("🚀 启动 Agent Status MCP 服务器...")
    print(f"📁 存储路径: ~/.task-manager/agent-sync-mcp/")
    print("🔧 可用工具:")
    print("   - update_agent_status: 更新 agent 状态")
    print("   - get_agent_status: 获取 agent 状态")
    print("   - get_task_status: 获取任务状态")
    print("   - list_active_agents: 列出活跃 agents")
    print("   - get_storage_info: 获取存储信息")
    print()
    
    try:
        mcp.run()
    except KeyboardInterrupt:
        print("\n👋 MCP 服务器已停止")
    except Exception as e:
        print(f"❌ 服务器启动失败: {e}")
        sys.exit(1)