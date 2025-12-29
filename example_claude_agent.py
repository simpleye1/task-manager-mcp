#!/usr/bin/env python3
"""
Claude Agent 正确使用 MCP 的完整示例
展示如何先初始化会话，然后使用正确的枚举值
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any, Optional


class SmartClaudeAgentMCPClient:
    """
    智能的 Claude Agent MCP 客户端
    会先初始化会话以获取可用的枚举值
    """
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.current_task_id: Optional[str] = None
        self.available_statuses: Dict[str, str] = {}
        self.available_actions: Dict[str, str] = {}
        self.initialized = False
    
    async def initialize_session(self):
        """初始化会话，获取可用的枚举值"""
        print(f"🔧 初始化 Agent 会话: {self.agent_id}")
        
        # 模拟调用 initialize_agent_session MCP 工具
        session_info = {
            "success": True,
            "data": {
                "agent_id": self.agent_id,
                "session_initialized": True,
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
                        "agent_id": self.agent_id,
                        "task_id": "task-example-001",
                        "status": "running",
                        "current_action": "code_writing",
                        "progress_percentage": 50,
                        "message": "正在编写用户认证功能"
                    }
                }
            }
        }
        
        if session_info["success"]:
            data = session_info["data"]
            self.available_statuses = data["available_options"]["task_statuses"]
            self.available_actions = data["available_options"]["agent_actions"]
            self.initialized = True
            
            print("✅ 会话初始化成功")
            print(f"   可用状态: {list(self.available_statuses.keys())}")
            print(f"   可用动作: {list(self.available_actions.keys())}")
            print()
        else:
            print("❌ 会话初始化失败")
            raise Exception("Failed to initialize session")
    
    async def start_task(self, task_description: str) -> str:
        """开始新任务"""
        if not self.initialized:
            await self.initialize_session()
        
        task_id = f"task-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        self.current_task_id = task_id
        
        # 使用正确的枚举值
        await self.update_status(
            task_id=task_id,
            status="pending",  # 从 available_statuses 中选择
            message=f"开始任务: {task_description}",
            progress_percentage=0,
            details={"task_description": task_description}
        )
        
        return task_id
    
    async def update_status(
        self,
        task_id: str,
        status: str,
        message: str,
        current_action: Optional[str] = None,
        progress_percentage: float = 0.0,
        details: Optional[Dict[str, Any]] = None
    ):
        """更新状态 - 使用验证过的枚举值"""
        if not self.initialized:
            await self.initialize_session()
        
        # 验证状态值
        if status not in self.available_statuses:
            raise ValueError(f"无效的状态: {status}. 可用状态: {list(self.available_statuses.keys())}")
        
        # 验证动作值
        if current_action and current_action not in self.available_actions:
            raise ValueError(f"无效的动作: {current_action}. 可用动作: {list(self.available_actions.keys())}")
        
        status_data = {
            "agent_id": self.agent_id,
            "task_id": task_id,
            "status": status,
            "current_action": current_action,
            "progress_percentage": progress_percentage,
            "message": message,
            "details": details or {},
            "timestamp": datetime.now().isoformat()
        }
        
        # 在实际使用中，这里会调用 MCP 的 update_agent_status 工具
        status_desc = self.available_statuses[status]
        action_desc = self.available_actions.get(current_action, "无") if current_action else "无"
        
        print(f"📊 [{self.agent_id}] {message} ({progress_percentage}%)")
        print(f"   状态: {status} ({status_desc})")
        print(f"   动作: {current_action or '无'} ({action_desc})")
        if details:
            print(f"   详情: {json.dumps(details, ensure_ascii=False, indent=2)}")
        print()
        
        # 模拟网络延迟
        await asyncio.sleep(0.1)
    
    async def complete_task(self, success: bool = True, final_details: Optional[Dict[str, Any]] = None):
        """完成任务"""
        if not self.current_task_id:
            return
        
        status = "completed" if success else "failed"
        message = "任务成功完成" if success else "任务执行失败"
        
        await self.update_status(
            task_id=self.current_task_id,
            status=status,
            message=message,
            progress_percentage=100,
            details=final_details or {}
        )
        
        self.current_task_id = None


class SmartCodeWritingAgent:
    """智能代码编写 Agent 示例"""
    
    def __init__(self, agent_id: str = "claude-smart-coder-001"):
        self.mcp_client = SmartClaudeAgentMCPClient(agent_id)
    
    async def write_feature(self, feature_description: str, repository: str):
        """编写新功能的完整流程 - 使用正确的枚举值"""
        print(f"🤖 智能 Claude Agent 开始编写功能: {feature_description}")
        print(f"📁 目标仓库: {repository}")
        print()
        
        # 1. 开始任务（会自动初始化会话）
        task_id = await self.mcp_client.start_task(f"编写功能: {feature_description}")
        
        # 2. 代码分析阶段
        await self.mcp_client.update_status(
            task_id=task_id,
            status="running",  # 使用验证过的枚举值
            current_action="code_analysis",  # 使用验证过的枚举值
            progress_percentage=10,
            message="分析现有代码结构",
            details={
                "repository": repository,
                "feature": feature_description,
                "analysis_started": True
            }
        )
        
        await asyncio.sleep(1)
        
        # 3. 代码编写阶段
        await self.mcp_client.update_status(
            task_id=task_id,
            status="running",
            current_action="code_writing",
            progress_percentage=40,
            message="开始编写功能代码",
            details={
                "files_to_modify": ["src/main.py", "src/utils.py", "src/models.py"],
                "estimated_lines": 150,
                "complexity": "medium"
            }
        )
        
        await asyncio.sleep(2)
        
        # 4. 代码审查阶段
        await self.mcp_client.update_status(
            task_id=task_id,
            status="running",
            current_action="code_review",
            progress_percentage=70,
            message="进行代码自审查",
            details={
                "files_written": 3,
                "lines_added": 145,
                "functions_added": ["process_feature", "validate_input", "handle_errors"],
                "review_issues": 2
            }
        )
        
        await asyncio.sleep(1)
        
        # 5. 测试阶段
        await self.mcp_client.update_status(
            task_id=task_id,
            status="running",
            current_action="testing",
            progress_percentage=85,
            message="运行测试套件",
            details={
                "tests_run": 15,
                "tests_passed": 14,
                "tests_failed": 1,
                "coverage": "92%"
            }
        )
        
        await asyncio.sleep(1)
        
        # 6. 错误处理阶段
        await self.mcp_client.update_status(
            task_id=task_id,
            status="running",
            current_action="error_handling",
            progress_percentage=90,
            message="修复测试失败问题",
            details={
                "issue": "边界条件处理",
                "fix_applied": "添加输入验证"
            }
        )
        
        await asyncio.sleep(0.5)
        
        # 7. 创建 PR
        await self.mcp_client.update_status(
            task_id=task_id,
            status="running",
            current_action="pr_creation",
            progress_percentage=95,
            message="创建 Pull Request",
            details={
                "pr_title": f"Add {feature_description}",
                "branch": "feature/new-feature",
                "reviewers": ["team-lead", "senior-dev"]
            }
        )
        
        await asyncio.sleep(0.5)
        
        # 8. 完成任务
        await self.mcp_client.complete_task(
            success=True,
            final_details={
                "pr_url": f"https://github.com/{repository}/pull/123",
                "total_time": "8 minutes",
                "files_changed": 3,
                "lines_changed": 145,
                "tests_added": 5,
                "feature_complete": True
            }
        )
        
        print("✅ 功能开发完成！")


async def demonstrate_error_handling():
    """演示错误处理 - 使用无效枚举值"""
    print("\n" + "="*60)
    print("🚨 演示错误处理：使用无效枚举值")
    print("="*60)
    
    client = SmartClaudeAgentMCPClient("error-demo-agent")
    
    try:
        # 尝试使用无效状态
        await client.update_status(
            task_id="test-task",
            status="invalid_status",  # 无效状态
            message="测试无效状态"
        )
    except ValueError as e:
        print(f"❌ 捕获到预期错误: {e}")
    
    try:
        # 尝试使用无效动作
        await client.update_status(
            task_id="test-task",
            status="running",
            current_action="invalid_action",  # 无效动作
            message="测试无效动作"
        )
    except ValueError as e:
        print(f"❌ 捕获到预期错误: {e}")


async def main():
    """主函数 - 演示智能 Claude Agent 工作流程"""
    agent = SmartCodeWritingAgent()
    
    await agent.write_feature(
        feature_description="用户认证系统",
        repository="example/web-app"
    )
    
    # 演示错误处理
    await demonstrate_error_handling()
    
    print("\n" + "="*60)
    print("💡 关键改进:")
    print("1. ✅ Agent 会自动初始化会话获取可用枚举值")
    print("2. ✅ 使用前会验证状态和动作的有效性")
    print("3. ✅ 提供清晰的错误信息和可用选项")
    print("4. ✅ 显示每个枚举值的详细描述")
    print("5. ✅ 完全避免了使用无效枚举值的问题")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())