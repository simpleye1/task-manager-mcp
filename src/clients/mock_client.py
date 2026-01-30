#!/usr/bin/env python3
"""
Mock client implementation for testing
"""

from typing import Dict, Any, Optional
from datetime import datetime, timezone
import uuid

from src.clients.base_client import TaskManagerClientBase


class MockTaskManagerClient(TaskManagerClientBase):
    """Mock implementation for testing without real API"""
    
    def __init__(self):
        self._executions: Dict[str, Dict] = {}
        self._steps: Dict[str, Dict] = {}
    
    def patch_execution(
        self, 
        execution_id: str, 
        session_id: str
    ) -> Dict[str, Any]:
        """Update execution's session_id"""
        if execution_id not in self._executions:
            self._executions[execution_id] = {
                "execution_id": execution_id,
                "status": "running",
                "started_at": datetime.now(timezone.utc).isoformat()
            }
        
        self._executions[execution_id]["session_id"] = session_id
        
        return {
            "success": True,
            "data": self._executions[execution_id]
        }
    
    def create_step(
        self, 
        execution_id: str, 
        step_name: str,
        message: Optional[str] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new step for an execution"""
        step_id = str(uuid.uuid4())[:8]
        
        step = {
            "step_id": step_id,
            "execution_id": execution_id,
            "step_name": step_name,
            "status": status if status else "running",
            "message": message,
            "started_at": datetime.now(timezone.utc).isoformat()
        }
        
        self._steps[step_id] = step
        
        return {
            "success": True,
            "data": step
        }
    
    def patch_step(
        self, 
        execution_id: str, 
        step_id: str,
        status: Optional[str] = None,
        message: Optional[str] = None
    ) -> Dict[str, Any]:
        """Partially update a step"""
        if not status and not message:
            return {"success": False, "error": "No fields to update"}
        
        if step_id not in self._steps:
            return {"success": False, "error": f"Step {step_id} not found"}
        
        step = self._steps[step_id]
        if status:
            step["status"] = status
            if status in ("completed", "failed", "skipped"):
                step["completed_at"] = datetime.now(timezone.utc).isoformat()
        if message:
            step["message"] = message
        
        return {
            "success": True,
            "data": step
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Health check"""
        return {
            "success": True,
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": "mock-1.0.0"
        }
