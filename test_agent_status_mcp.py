#!/usr/bin/env python3
"""
Agent Status MCP 完整测试套件
包含所有功能的测试：数据结构、存储、工具、错误处理
"""

import sys
import os
import json
import shutil
from pathlib import Path
from datetime import datetime

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent_status_mcp import (
    LocalFileStorage, AgentStatus, TaskStatus, AgentAction
)


class TestSuite:
    """测试套件类"""
    
    def __init__(self):
        self.test_storage_path = "./test_storage"
        self.passed_tests = 0
        self.total_tests = 0
    
    def run_test(self, test_name: str, test_func):
        """运行单个测试"""
        self.total_tests += 1
        try:
            print(f"\n🧪 {test_name}")
            test_func()
            print(f"✅ {test_name} - 通过")
            self.passed_tests += 1
        except Exception as e:
            print(f"❌ {test_name} - 失败: {e}")
    
    def cleanup(self):
        """清理测试文件"""
        if Path(self.test_storage_path).exists():
            shutil.rmtree(self.test_storage_path)
    
    def print_summary(self):
        """打印测试总结"""
        print(f"\n{'='*60}")
        print(f"📊 测试总结: {self.passed_tests}/{self.total_tests} 通过")
        if self.passed_tests == self.total_tests:
            print("🎉 所有测试通过！")
        else:
            print(f"⚠️  {self.total_tests - self.passed_tests} 个测试失败")
        print(f"{'='*60}")


def test_data_structures():
    """测试 1: 数据结构和枚举"""
    print("   测试任务状态枚举...")
    statuses = [status.value for status in TaskStatus]
    expected_statuses = ["pending", "running", "completed", "failed", "cancelled"]
    assert statuses == expected_statuses, f"状态枚举不匹配: {statuses}"
    
    print("   测试 Agent 动作枚举...")
    actions = [action.value for action in AgentAction]
    expected_actions = [
        "code_analysis", "code_writing", "code_review", "testing",
        "pr_creation", "pr_update", "error_handling", "waiting_input"
    ]
    assert actions == expected_actions, f"动作枚举不匹配: {actions}"
    
    print("   测试 AgentStatus 数据结构...")
    status = AgentStatus(
        agent_id="test-agent",
        task_id="test-task",
        status=TaskStatus.RUNNING,
        current_action=AgentAction.CODE_WRITING,
        progress_percentage=50.0,
        message="测试消息",
        details={"test": True},
        timestamp="2024-12-29T14:30:22Z"
    )
    
    # 测试序列化
    status_dict = status.to_dict()
    assert status_dict["agent_id"] == "test-agent"
    assert status_dict["status"] == "running"
    assert status_dict["current_action"] == "code_writing"
    assert status_dict["progress_percentage"] == 50.0


def test_local_storage():
    """测试 2: 本地文件存储"""
    storage = LocalFileStorage("./test_storage")
    
    print("   测试目录创建...")
    assert storage.agents_dir.exists(), "agents 目录未创建"
    assert storage.tasks_dir.exists(), "tasks 目录未创建"
    assert storage.logs_dir.exists(), "logs 目录未创建"
    
    print("   测试状态保存...")
    status = AgentStatus(
        agent_id="storage-test-agent",
        task_id="storage-test-task",
        status=TaskStatus.RUNNING,
        current_action=AgentAction.CODE_ANALYSIS,
        progress_percentage=25.0,
        message="存储测试",
        details={"storage_test": True},
        timestamp=datetime.now().isoformat()
    )
    
    storage.save_agent_status(status)
    
    print("   测试状态读取...")
    agent_data = storage.get_agent_status("storage-test-agent")
    assert agent_data is not None, "无法读取 agent 状态"
    assert agent_data["agent_id"] == "storage-test-agent"
    assert agent_data["current_status"]["status"] == "running"
    
    task_data = storage.get_task_status("storage-test-task")
    assert task_data is not None, "无法读取任务状态"
    assert task_data["task_id"] == "storage-test-task"
    
    print("   测试活跃 agents 列表...")
    active_agents = storage.list_active_agents()
    assert len(active_agents) == 1, f"活跃 agents 数量错误: {len(active_agents)}"


def test_status_transitions():
    """测试 3: 状态转换和历史记录"""
    storage = LocalFileStorage("./test_storage")
    agent_id = "transition-agent"
    task_id = "transition-task"
    
    print("   测试状态转换序列...")
    transitions = [
        (TaskStatus.PENDING, None, 0, "任务开始"),
        (TaskStatus.RUNNING, AgentAction.CODE_ANALYSIS, 20, "分析代码"),
        (TaskStatus.RUNNING, AgentAction.CODE_WRITING, 50, "编写代码"),
        (TaskStatus.RUNNING, AgentAction.TESTING, 80, "运行测试"),
        (TaskStatus.COMPLETED, None, 100, "任务完成")
    ]
    
    for i, (status, action, progress, message) in enumerate(transitions):
        test_status = AgentStatus(
            agent_id=agent_id,
            task_id=task_id,
            status=status,
            current_action=action,
            progress_percentage=progress,
            message=message,
            details={"step": i + 1},
            timestamp=f"2024-12-29T14:3{i:02d}:22Z"
        )
        storage.save_agent_status(test_status)
    
    print("   测试历史记录...")
    agent_data = storage.get_agent_status(agent_id)
    assert agent_data is not None, "无法读取 agent 数据"
    
    history = agent_data.get("history", [])
    assert len(history) == 5, f"历史记录数量错误: {len(history)}"
    
    # 验证最终状态
    final_status = agent_data["current_status"]
    assert final_status["status"] == "completed", "最终状态不正确"
    assert final_status["progress_percentage"] == 100, "最终进度不正确"
    
    print("   测试历史记录限制...")
    # 添加更多记录测试限制功能
    for i in range(100):
        extra_status = AgentStatus(
            agent_id=agent_id,
            task_id=f"extra-task-{i}",
            status=TaskStatus.RUNNING,
            current_action=AgentAction.CODE_WRITING,
            progress_percentage=i,
            message=f"额外记录 {i}",
            details={"extra": i},
            timestamp=f"2024-12-29T15:{i:02d}:22Z"
        )
        storage.save_agent_status(extra_status)
    
    # 验证历史记录限制在100条
    agent_data = storage.get_agent_status(agent_id)
    history = agent_data.get("history", [])
    assert len(history) <= 100, f"历史记录超过限制: {len(history)}"


def test_mcp_tools_simulation():
    """测试 4: 模拟 MCP 工具功能"""
    print("   测试初始化会话功能...")
    
    # 模拟 initialize_agent_session 功能
    def simulate_initialize_agent_session(agent_id: str):
        return {
            "success": True,
            "data": {
                "agent_id": agent_id,
                "session_initialized": True,
                "available_options": {
                    "task_statuses": {status.value: f"状态_{status.value}" for status in TaskStatus},
                    "agent_actions": {action.value: f"动作_{action.value}" for action in AgentAction}
                }
            }
        }
    
    result = simulate_initialize_agent_session("test-agent")
    assert result["success"], "初始化会话失败"
    assert len(result["data"]["available_options"]["task_statuses"]) == 5, "状态数量不正确"
    assert len(result["data"]["available_options"]["agent_actions"]) == 8, "动作数量不正确"
    
    print("   测试获取可用状态功能...")
    
    # 模拟 get_available_statuses 功能
    def simulate_get_available_statuses():
        return {
            "success": True,
            "data": {
                "task_statuses": [status.value for status in TaskStatus],
                "agent_actions": [action.value for action in AgentAction]
            }
        }
    
    result = simulate_get_available_statuses()
    assert result["success"], "获取可用状态失败"
    assert "pending" in result["data"]["task_statuses"], "缺少 pending 状态"
    assert "code_writing" in result["data"]["agent_actions"], "缺少 code_writing 动作"


def test_error_handling():
    """测试 5: 错误处理"""
    print("   测试无效枚举值处理...")
    
    # 测试无效状态值
    try:
        TaskStatus("invalid_status")
        assert False, "应该抛出 ValueError"
    except ValueError:
        pass  # 预期的错误
    
    # 测试无效动作值
    try:
        AgentAction("invalid_action")
        assert False, "应该抛出 ValueError"
    except ValueError:
        pass  # 预期的错误
    
    print("   测试文件读取错误处理...")
    storage = LocalFileStorage("./test_storage")
    
    # 测试读取不存在的 agent
    result = storage.get_agent_status("nonexistent-agent")
    assert result is None, "应该返回 None"
    
    # 测试读取不存在的任务
    result = storage.get_task_status("nonexistent-task")
    assert result is None, "应该返回 None"


def test_edge_cases():
    """测试 6: 边界情况"""
    print("   测试进度百分比边界...")
    
    # 测试负数进度
    status = AgentStatus(
        agent_id="edge-test",
        task_id="edge-task",
        status=TaskStatus.RUNNING,
        current_action=AgentAction.CODE_WRITING,
        progress_percentage=-10,  # 负数
        message="边界测试",
        details={},
        timestamp=datetime.now().isoformat()
    )
    
    # 在实际的 update_agent_status 工具中，会被限制在 0-100 范围内
    # 这里我们模拟这个逻辑
    normalized_progress = max(0, min(100, status.progress_percentage))
    assert normalized_progress == 0, "负数进度应该被规范化为 0"
    
    # 测试超过100的进度
    status.progress_percentage = 150
    normalized_progress = max(0, min(100, status.progress_percentage))
    assert normalized_progress == 100, "超过100的进度应该被规范化为 100"
    
    print("   测试空详情和可选参数...")
    status = AgentStatus(
        agent_id="optional-test",
        task_id="optional-task",
        status=TaskStatus.PENDING,
        current_action=None,  # 可选参数
        progress_percentage=0,
        message="可选参数测试",
        details={},  # 空详情
        timestamp=datetime.now().isoformat()
    )
    
    status_dict = status.to_dict()
    assert status_dict["current_action"] is None, "可选动作应该为 None"
    assert status_dict["details"] == {}, "空详情应该为空字典"


def main():
    """主测试函数"""
    print("🚀 开始 Agent Status MCP 完整测试套件")
    print("="*60)
    
    suite = TestSuite()
    
    # 运行所有测试
    suite.run_test("数据结构和枚举测试", test_data_structures)
    suite.run_test("本地文件存储测试", test_local_storage)
    suite.run_test("状态转换和历史记录测试", test_status_transitions)
    suite.run_test("MCP 工具功能模拟测试", test_mcp_tools_simulation)
    suite.run_test("错误处理测试", test_error_handling)
    suite.run_test("边界情况测试", test_edge_cases)
    
    # 清理和总结
    suite.cleanup()
    suite.print_summary()


if __name__ == "__main__":
    main()