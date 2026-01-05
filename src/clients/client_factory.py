#!/usr/bin/env python3
"""
Factory for creating Task Manager clients
"""

import os

# Import from local modules
import sys
from pathlib import Path
clients_path = Path(__file__).parent.parent / "clients"
sys.path.insert(0, str(clients_path))

from mock_client import MockTaskManagerClient
from http_client import HttpTaskManagerClient


def create_task_manager_client():
    """Factory method to create Task Manager client"""
    # Use mock client if in test mode
    if os.getenv('USE_MOCK_CLIENT', 'false').lower() == 'true':
        return MockTaskManagerClient()
    
    # Default to HTTP client
    return HttpTaskManagerClient()