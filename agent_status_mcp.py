#!/usr/bin/env python3
"""
Agent Status MCP Server
用于跟踪 Claude agent 执行状态的 MCP 服务器

数据模型说明：
- Agent: 执行任务的智能体（如 claude-coder-001）
- Task: Agent 执行的具体任务（如编写某个功能）
- 一个 Agent 可以执行多个 Task，但同时只能有一个活跃的 Task

存储路径可通过环境变量 AGENT_STATUS_STORAGE_PATH 配置，默认为 ~/.task-manager/agent-status
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

import fastmcp


class TaskStatus(Enum):
    """任务状态枚举 - 简化为三种状态"""
    RUNNING = "running"
    SUCCESS = "success" 
    FAILED = "failed"


@dataclass
class TaskInfo:
    """任务信息数据结构"""
    task_id: str
    agent_id: str
    status: TaskStatus
    current_action: str  # Agent 自定义的当前动作描述
    progress_percentage: float  # 0-100
    message: str
    details: Dict[str, Any]  # 额外的任务详情
    created_at: str
    updated_at: str
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "task_id": self.task_id,
            "agent_id": self.agent_id,
            "status": self.status.value,
            "current_action": self.current_action,
            "progress_percentage": self.progress_percentage,
            "message": self.message,
            "details": self.details,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class StatusStorage:
    """状态存储管理器"""
    
    def __init__(self, base_path: Optional[str] = None):
        # 支持通过环境变量或参数配置存储路径
        if base_path is None:
            base_path = os.getenv('AGENT_STATUS_STORAGE_PATH', '~/.task-manager/agent-status')
        
        self.base_path = Path(base_path).expanduser()
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # 创建存储目录
        self.tasks_dir = self.base_path / "tasks"
        self.agents_dir = self.base_path / "agents"
        
        for dir_path in [self.tasks_dir, self.agents_dir]:
            dir_path.mkdir(exist_ok=True)
    
    def save_task(self, task: TaskInfo) -> None:
        """保存任务状态"""
        # 保存任务文件
        task_file = self.tasks_dir / f"{task.task_id}.json"
        with open(task_file, 'w', encoding='utf-8') as f:
            json.dump(task.to_dict(), f, indent=2, ensure_ascii=False)
        
        # 更新 Agent 的当前任务
        self._update_agent_current_task(task)
    
    def _update_agent_current_task(self, task: TaskInfo) -> None:
        """更新 Agent 的当前任务信息"""
        agent_file = self.agents_dir / f"{task.agent_id}.json"
        
        # 读取现有 Agent 数据
        agent_data = {}
        if agent_file.exists():
            try:
                with open(agent_file, 'r', encoding='utf-8') as f:
                    agent_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                agent_data = {}
        
        # 更新 Agent 数据
        agent_data.update({
            "agent_id": task.agent_id,
            "current_task": task.to_dict(),
            "last_updated": task.updated_at
        })
        
        # 保存 Agent 数据
        with open(agent_file, 'w', encoding='utf-8') as f:
            json.dump(agent_data, f, indent=2, ensure_ascii=False)
    
    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """获取任务状态"""
        task_file = self.tasks_dir / f"{task_id}.json"
        if not task_file.exists():
            return None
        
        try:
            with open(task_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return None
    
    def get_agent_current_task(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """获取 Agent 当前任务"""
        agent_file = self.agents_dir / f"{agent_id}.json"
        if not agent_file.exists():
            return None
        
        try:
            with open(agent_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return None
    
    def list_running_tasks(self) -> List[Dict[str, Any]]:
        """列出所有运行中的任务"""
        running_tasks = []
        for task_file in self.tasks_dir.glob("*.json"):
            try:
                with open(task_file, 'r', encoding='utf-8') as f:
                    task_data = json.load(f)
                    if task_data.get('status') == 'running':
                        running_tasks.append(task_data)
            except (json.JSONDecodeError, KeyError):
                continue
        return running_tasks
    
    def get_storage_info(self) -> Dict[str, Any]:
        """获取存储信息"""
        tasks_count = len(list(self.tasks_dir.glob("*.json")))
        agents_count = len(list(self.agents_dir.glob("*.json")))
        
        return {
            "storage_path": str(self.base_path),
            "tasks_count": tasks_count,
            "agents_count": agents_count,
            "running_tasks": len(self.list_running_tasks())
        }


# 初始化存储
storage = StatusStorage()

# 创建 FastMCP 应用
mcp = fastmcp.FastMCP("Agent Status Tracker")


@mcp.tool()
def update_task_status(
    task_id: str,
    agent_id: str,
    status: str,
    current_action: str,
    message: str,
    progress_percentage: float = 0.0,
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    更新任务状态
    
    Args:
        task_id: 任务唯一标识符
        agent_id: 执行任务的 Agent 标识符
        status: 任务状态 (running/success/failed)
        current_action: 当前执行的动作描述 (Agent 自定义字符串)
        message: 状态描述信息
        progress_percentage: 进度百分比 (0-100)
        details: 额外的任务详情 (可选)
    
    Returns:
        操作结果
    """
    try:
        # 验证状态值
        task_status = TaskStatus(status)
        
        # 获取现有任务信息（如果存在）
        existing_task = storage.get_task(task_id)
        created_at = existing_task.get('created_at') if existing_task else datetime.now(timezone.utc).isoformat()
        
        # 创建任务对象
        task = TaskInfo(
            task_id=task_id,
            agent_id=agent_id,
            status=task_status,
            current_action=current_action,
            progress_percentage=max(0, min(100, progress_percentage)),
            message=message,
            details=details or {},
            created_at=created_at,
            updated_at=datetime.now(timezone.utc).isoformat()
        )
        
        # 保存任务
        storage.save_task(task)
        
        return {
            "success": True,
            "message": f"任务 {task_id} 状态已更新",
            "task": task.to_dict()
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
def get_task_status(task_id: str) -> Dict[str, Any]:
    """
    获取任务状态
    
    Args:
        task_id: 任务唯一标识符
    
    Returns:
        任务状态信息
    """
    try:
        task_data = storage.get_task(task_id)
        if task_data is None:
            return {
                "success": False,
                "error": f"未找到任务 {task_id}"
            }
        
        return {
            "success": True,
            "task": task_data
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"获取任务状态失败: {str(e)}"
        }


@mcp.tool()
def get_agent_status(agent_id: str) -> Dict[str, Any]:
    """
    获取 Agent 当前状态
    
    Args:
        agent_id: Agent 唯一标识符
    
    Returns:
        Agent 当前任务信息
    """
    try:
        agent_data = storage.get_agent_current_task(agent_id)
        if agent_data is None:
            return {
                "success": False,
                "error": f"未找到 Agent {agent_id} 的状态信息"
            }
        
        return {
            "success": True,
            "agent": agent_data
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"获取 Agent 状态失败: {str(e)}"
        }


@mcp.tool()
def list_running_tasks() -> Dict[str, Any]:
    """
    列出所有运行中的任务
    
    Returns:
        运行中的任务列表
    """
    try:
        tasks = storage.list_running_tasks()
        return {
            "success": True,
            "running_tasks": tasks,
            "count": len(tasks)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"获取运行中任务失败: {str(e)}"
        }


@mcp.tool()
def get_storage_info() -> Dict[str, Any]:
    """
    获取存储信息和统计
    
    Returns:
        存储信息
    """
    try:
        info = storage.get_storage_info()
        return {
            "success": True,
            "storage_info": info
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"获取存储信息失败: {str(e)}"
        }


if __name__ == "__main__":
    mcp.run()