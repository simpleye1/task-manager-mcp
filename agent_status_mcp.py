#!/usr/bin/env python3
"""
Agent Status MCP Server
用于跟踪 Claude agent 执行状态的 MCP 服务器
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

import fastmcp


class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = "pending"
    RUNNING = "running" 
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentAction(Enum):
    """Agent 动作类型"""
    CODE_ANALYSIS = "code_analysis"
    CODE_WRITING = "code_writing"
    CODE_REVIEW = "code_review"
    TESTING = "testing"
    PR_CREATION = "pr_creation"
    PR_UPDATE = "pr_update"
    ERROR_HANDLING = "error_handling"
    WAITING_INPUT = "waiting_input"


@dataclass
class AgentStatus:
    """Agent 状态数据结构"""
    agent_id: str
    task_id: str
    status: TaskStatus
    current_action: Optional[AgentAction]
    progress_percentage: float  # 0-100
    message: str
    details: Dict[str, Any]  # 额外的状态详情
    timestamp: str
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "agent_id": self.agent_id,
            "task_id": self.task_id,
            "status": self.status.value,
            "current_action": self.current_action.value if self.current_action else None,
            "progress_percentage": self.progress_percentage,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp
        }


class LocalFileStorage:
    """本地文件存储管理器"""
    
    def __init__(self, base_path: str = "~/.task-manager/agent-sync-mcp"):
        self.base_path = Path(base_path).expanduser()
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # 创建子目录
        self.agents_dir = self.base_path / "agents"
        self.tasks_dir = self.base_path / "tasks"
        self.logs_dir = self.base_path / "logs"
        
        for dir_path in [self.agents_dir, self.tasks_dir, self.logs_dir]:
            dir_path.mkdir(exist_ok=True)
    
    def save_agent_status(self, status: AgentStatus) -> None:
        """保存 agent 状态"""
        # 保存到 agent 专用文件
        agent_file = self.agents_dir / f"{status.agent_id}.json"
        
        # 读取现有状态历史
        history = []
        if agent_file.exists():
            try:
                with open(agent_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    history = data.get('history', [])
            except (json.JSONDecodeError, KeyError):
                history = []
        
        # 添加新状态到历史
        history.append(status.to_dict())
        
        # 保持最近100条记录
        if len(history) > 100:
            history = history[-100:]
        
        # 保存更新后的数据
        agent_data = {
            "agent_id": status.agent_id,
            "current_status": status.to_dict(),
            "last_updated": status.timestamp,
            "history": history
        }
        
        with open(agent_file, 'w', encoding='utf-8') as f:
            json.dump(agent_data, f, indent=2, ensure_ascii=False)
        
        # 同时保存到任务文件
        self._save_task_status(status)
    
    def _save_task_status(self, status: AgentStatus) -> None:
        """保存任务状态"""
        task_file = self.tasks_dir / f"{status.task_id}.json"
        
        task_data = {
            "task_id": status.task_id,
            "agent_id": status.agent_id,
            "current_status": status.to_dict(),
            "last_updated": status.timestamp
        }
        
        with open(task_file, 'w', encoding='utf-8') as f:
            json.dump(task_data, f, indent=2, ensure_ascii=False)
    
    def get_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """获取 agent 当前状态"""
        agent_file = self.agents_dir / f"{agent_id}.json"
        if not agent_file.exists():
            return None
        
        try:
            with open(agent_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return None
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """获取任务状态"""
        task_file = self.tasks_dir / f"{task_id}.json"
        if not task_file.exists():
            return None
        
        try:
            with open(task_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return None
    
    def list_active_agents(self) -> List[Dict[str, Any]]:
        """列出所有活跃的 agents"""
        agents = []
        for agent_file in self.agents_dir.glob("*.json"):
            try:
                with open(agent_file, 'r', encoding='utf-8') as f:
                    agent_data = json.load(f)
                    current_status = agent_data.get('current_status', {})
                    # 只返回非完成状态的 agents
                    if current_status.get('status') not in ['completed', 'failed', 'cancelled']:
                        agents.append(agent_data)
            except (json.JSONDecodeError, KeyError):
                continue
        return agents


# 初始化存储
storage = LocalFileStorage()

# 创建 FastMCP 应用
mcp = fastmcp.FastMCP("Agent Status Tracker")


@mcp.tool()
def update_agent_status(
    agent_id: str,
    task_id: str,
    status: str,
    message: str,
    current_action: Optional[str] = None,
    progress_percentage: float = 0.0,
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    更新 agent 状态
    
    Args:
        agent_id: Agent 唯一标识符
        task_id: 任务唯一标识符  
        status: 任务状态，可选值: pending, running, completed, failed, cancelled
        message: 状态描述信息
        current_action: 当前执行的动作类型，可选值: code_analysis, code_writing, code_review, testing, pr_creation, pr_update, error_handling, waiting_input
        progress_percentage: 进度百分比 (0-100)
        details: 额外的状态详情 (可选)
    
    Returns:
        操作结果
        
    Note:
        使用 get_available_statuses() 工具可以获取所有可用的状态和动作类型
    """
    try:
        # 验证状态值
        task_status = TaskStatus(status)
        agent_action = AgentAction(current_action) if current_action else None
        
        # 创建状态对象
        agent_status = AgentStatus(
            agent_id=agent_id,
            task_id=task_id,
            status=task_status,
            current_action=agent_action,
            progress_percentage=max(0, min(100, progress_percentage)),
            message=message,
            details=details or {},
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        
        # 保存状态
        storage.save_agent_status(agent_status)
        
        return {
            "success": True,
            "message": f"Agent {agent_id} 状态已更新",
            "status": agent_status.to_dict()
        }
        
    except ValueError as e:
        return {
            "success": False,
            "error": f"无效的状态值: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"更新状态失败: {str(e)}"
        }


@mcp.tool()
def get_agent_status(agent_id: str) -> Dict[str, Any]:
    """
    获取指定 agent 的当前状态和历史
    
    Args:
        agent_id: Agent 唯一标识符
    
    Returns:
        Agent 状态信息
    """
    try:
        agent_data = storage.get_agent_status(agent_id)
        if agent_data is None:
            return {
                "success": False,
                "error": f"未找到 Agent {agent_id} 的状态信息"
            }
        
        return {
            "success": True,
            "data": agent_data
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"获取状态失败: {str(e)}"
        }


@mcp.tool()
def get_task_status(task_id: str) -> Dict[str, Any]:
    """
    获取指定任务的状态
    
    Args:
        task_id: 任务唯一标识符
    
    Returns:
        任务状态信息
    """
    try:
        task_data = storage.get_task_status(task_id)
        if task_data is None:
            return {
                "success": False,
                "error": f"未找到任务 {task_id} 的状态信息"
            }
        
        return {
            "success": True,
            "data": task_data
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"获取任务状态失败: {str(e)}"
        }


@mcp.tool()
def list_active_agents() -> Dict[str, Any]:
    """
    列出所有活跃的 agents
    
    Returns:
        活跃 agents 列表
    """
    try:
        agents = storage.list_active_agents()
        return {
            "success": True,
            "data": {
                "active_agents": agents,
                "count": len(agents)
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"获取活跃 agents 失败: {str(e)}"
        }


@mcp.tool()
def initialize_agent_session(agent_id: str) -> Dict[str, Any]:
    """
    初始化 agent 会话，返回所有必要的配置信息
    
    Args:
        agent_id: Agent 唯一标识符
    
    Returns:
        初始化信息，包括可用状态、动作类型和使用指南
    """
    try:
        return {
            "success": True,
            "data": {
                "agent_id": agent_id,
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
                    "workflow": [
                        "1. 使用 update_agent_status 更新状态",
                        "2. status 参数使用上述 task_statuses 中的键值",
                        "3. current_action 参数使用上述 agent_actions 中的键值",
                        "4. progress_percentage 范围是 0-100",
                        "5. details 可以包含任意额外信息"
                    ],
                    "example": {
                        "agent_id": agent_id,
                        "task_id": "task-example-001",
                        "status": "running",
                        "current_action": "code_writing",
                        "progress_percentage": 50,
                        "message": "正在编写用户认证功能",
                        "details": {
                            "files_modified": ["auth.py", "models.py"],
                            "estimated_completion": "10 minutes"
                        }
                    }
                },
                "storage_path": str(storage.base_path)
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"初始化会话失败: {str(e)}"
        }


@mcp.tool()
def get_available_statuses() -> Dict[str, Any]:
    """
    获取所有可用的状态和动作类型
    
    Returns:
        可用的状态和动作枚举值
    """
    try:
        return {
            "success": True,
            "data": {
                "task_statuses": [status.value for status in TaskStatus],
                "agent_actions": [action.value for action in AgentAction],
                "task_status_descriptions": {
                    "pending": "等待执行",
                    "running": "正在执行", 
                    "completed": "已完成",
                    "failed": "执行失败",
                    "cancelled": "已取消"
                },
                "agent_action_descriptions": {
                    "code_analysis": "代码分析",
                    "code_writing": "代码编写",
                    "code_review": "代码审查",
                    "testing": "测试执行",
                    "pr_creation": "创建 Pull Request",
                    "pr_update": "更新 Pull Request",
                    "error_handling": "错误处理",
                    "waiting_input": "等待输入"
                }
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"获取可用状态失败: {str(e)}"
        }


@mcp.tool()
def get_storage_info() -> Dict[str, Any]:
    """
    获取存储信息和统计
    
    Returns:
        存储信息
    """
    try:
        agents_count = len(list(storage.agents_dir.glob("*.json")))
        tasks_count = len(list(storage.tasks_dir.glob("*.json")))
        
        return {
            "success": True,
            "data": {
                "storage_path": str(storage.base_path),
                "agents_count": agents_count,
                "tasks_count": tasks_count,
                "directories": {
                    "agents": str(storage.agents_dir),
                    "tasks": str(storage.tasks_dir),
                    "logs": str(storage.logs_dir)
                }
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"获取存储信息失败: {str(e)}"
        }


if __name__ == "__main__":
    mcp.run()