#!/usr/bin/env python3
"""
HTTP client implementation for Task Manager API
"""

import os
from typing import Dict, Any, Optional
import httpx

from src.clients.base_client import TaskManagerClientBase


class HttpTaskManagerClient(TaskManagerClientBase):
    """HTTP implementation for Task Manager API"""
    
    def __init__(self):
        self.host = os.getenv('TASK_MANAGER_HOST', 'localhost')
        self.port = os.getenv('TASK_MANAGER_PORT', '8080')
        self.base_url = f"http://{self.host}:{self.port}"
        self.timeout = int(os.getenv('TASK_MANAGER_TIMEOUT', '30'))
    
    def _make_request(
        self, 
        method: str, 
        path: str, 
        json_data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make HTTP request and handle response"""
        try:
            with httpx.Client(base_url=self.base_url, timeout=self.timeout) as client:
                response = client.request(
                    method=method,
                    url=path,
                    json=json_data
                )
                
                if response.status_code >= 400:
                    error_data = response.json()
                    return {
                        "success": False,
                        "error": error_data.get("error", "Unknown error"),
                        "error_code": error_data.get("error_code"),
                        "status_code": response.status_code
                    }
                
                return response.json()
                
        except httpx.TimeoutException:
            return {"success": False, "error": "Request timeout"}
        except httpx.ConnectError:
            return {"success": False, "error": f"Connection failed to {self.base_url}"}
        except Exception as e:
            return {"success": False, "error": f"Request failed: {str(e)}"}
    
    def patch_execution(
        self, 
        execution_id: str, 
        session_id: str
    ) -> Dict[str, Any]:
        """Update execution's session_id"""
        return self._make_request(
            "PATCH",
            f"/api/executions/{execution_id}",
            json_data={"session_id": session_id}
        )
    
    def create_step(
        self, 
        execution_id: str, 
        step_name: str,
        message: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new step for an execution"""
        body = {"step_name": step_name}
        if message is not None:
            body["message"] = message
        
        return self._make_request(
            "POST",
            f"/api/executions/{execution_id}/steps",
            json_data=body
        )
    
    def patch_step(
        self, 
        execution_id: str, 
        step_id: str,
        status: Optional[str] = None,
        message: Optional[str] = None
    ) -> Dict[str, Any]:
        """Partially update a step"""
        body = {}
        if status is not None:
            body["status"] = status
        if message is not None:
            body["message"] = message
        
        if not body:
            return {"success": False, "error": "No fields to update"}
        
        return self._make_request(
            "PATCH",
            f"/api/executions/{execution_id}/steps/{step_id}",
            json_data=body
        )
    
    def health_check(self) -> Dict[str, Any]:
        """Health check"""
        result = self._make_request("GET", "/api/health")
        if result.get("success", True) and "error" not in result:
            return {
                "success": True,
                "message": "Task Manager service is healthy",
                "config": {
                    "host": self.host,
                    "port": self.port,
                    "base_url": self.base_url
                },
                **result
            }
        return result
