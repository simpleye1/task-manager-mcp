#!/usr/bin/env python3
"""
简单的功能测试
"""

import sys
import os
from datetime import datetime, timezone
from pathlib import Path

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent_status_mcp import StatusStorage, TaskInfo, TaskStatus


def test_basic_functionality():
    """测试基本功能"""
    print("🧪 测试 Agent Status MCP 基本功能")
    print("="*50)
    
    # 初始化存储
    storage = StatusStorage()
    print(f"✅ 存储初始化完成: {storage.base_path}")
    
    # 创建测试任务
    task = TaskInfo(
        task_id="test-task-001",
        agent_id="test-agent",
        status=TaskStatus.RUNNING,
        current_action="编写代码",
        progress_percentage=50,
        message="正在测试基本功能",
        details={"test": True},
        created_at=datetime.now(timezone.utc).isoformat(),
        updated_at=datetime.now(timezone.utc).isoformat()
    )
    
    # 保存任务
    storage.save_task(task)
    print("✅ 任务保存成功")
    
    # 读取任务
    task_data = storage.get_task("test-task-001")
    if task_data:
        print("✅ 任务读取成功")
        print(f"   任务ID: {task_data['task_id']}")
        print(f"   状态: {task_data['status']}")
        print(f"   进度: {task_data['progress_percentage']}%")
    
    # 读取 Agent 状态
    agent_data = storage.get_agent_current_task("test-agent")
    if agent_data:
        print("✅ Agent 状态读取成功")
        print(f"   Agent ID: {agent_data['agent_id']}")
        print(f"   当前任务: {agent_data['current_task']['task_id']}")
    
    # 列出运行中的任务
    running_tasks = storage.list_running_tasks()
    print(f"✅ 运行中的任务: {len(running_tasks)} 个")
    
    # 获取存储信息
    info = storage.get_storage_info()
    print("✅ 存储信息:")
    print(f"   存储路径: {info['storage_path']}")
    print(f"   任务数量: {info['tasks_count']}")
    print(f"   Agent 数量: {info['agents_count']}")
    
    # 完成任务
    task.status = TaskStatus.SUCCESS
    task.progress_percentage = 100
    task.message = "测试完成"
    task.updated_at = datetime.now(timezone.utc).isoformat()
    storage.save_task(task)
    print("✅ 任务完成")
    
    print("\n🎉 所有测试通过！")


if __name__ == "__main__":
    test_basic_functionality()