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
    print(f"📁 存储路径: ~/.task-manager/agent-status/")
    print("   (可通过环境变量 AGENT_STATUS_STORAGE_PATH 配置)")
    print("🔧 可用工具:")
    print("   - update_task_status: 更新任务状态")
    print("   - get_task_status: 获取任务状态")
    print("   - get_agent_status: 获取 Agent 状态")
    print("   - list_running_tasks: 列出运行中的任务")
    print("   - get_storage_info: 获取存储信息")
    print()
    
    try:
        mcp.run()
    except KeyboardInterrupt:
        print("\n👋 MCP 服务器已停止")
    except Exception as e:
        print(f"❌ 服务器启动失败: {e}")
        sys.exit(1)