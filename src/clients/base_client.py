#!/usr/bin/env python3
"""
Base client interface for Task Manager clients
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class TaskManagerClientBase(ABC):
    """Abstract base class defining the Task Manager client interface"""
    
    @abstractmethod
    def patch_execution(
        self, 
        execution_id: str, 
        session_id: str
    ) -> Dict[str, Any]:
        """Update execution's session_id
        
        Args:
            execution_id: Execution identifier
            session_id: Session ID to set
            
        Returns:
            Dict with 'success' bool and execution data or 'error'
        """
        pass
    
    @abstractmethod
    def create_step(
        self, 
        execution_id: str, 
        step_name: str,
        message: Optional[str] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new step for an execution
        
        Args:
            execution_id: Execution identifier
            step_name: Name of the step
            message: Optional message for the step
            status: Optional initial status (default: "running")
            
        Returns:
            Dict with 'success' bool and step data or 'error'
        """
        pass
    
    @abstractmethod
    def patch_step(
        self, 
        execution_id: str, 
        step_id: str,
        status: Optional[str] = None,
        message: Optional[str] = None
    ) -> Dict[str, Any]:
        """Partially update a step
        
        Args:
            execution_id: Execution identifier
            step_id: Step identifier
            status: New status (optional)
            message: New message (optional)
            
        Returns:
            Dict with 'success' bool and step data or 'error'
        """
        pass
    
    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """Check service health
        
        Returns:
            Dict with 'success' bool and health information
        """
        pass
