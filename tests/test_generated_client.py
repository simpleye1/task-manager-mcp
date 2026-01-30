#!/usr/bin/env python3
"""
Test generated HTTP client
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.clients import create_task_manager_client


def test_generated_client():
    """Test the HTTP client"""
    print("Testing Client with Mock...")
    
    # Use mock client for testing
    os.environ['USE_MOCK_CLIENT'] = 'true'
    client = create_task_manager_client()
    print(f"Created client: {type(client).__name__}")
    
    # Test health check
    print("\n1. Testing health check...")
    health_result = client.health_check()
    print(f"Health check result: {health_result}")
    assert health_result.get("success") == True, "Health check should succeed"
    
    # Test patch execution
    print("\n2. Testing patch execution...")
    patch_result = client.patch_execution(
        execution_id="test-exec-123",
        session_id="test-session-456"
    )
    print(f"Patch execution result: {patch_result}")
    assert patch_result.get("success") == True, "Patch execution should succeed"
    
    # Test create step
    print("\n3. Testing create step...")
    create_result = client.create_step(
        execution_id="test-exec-123",
        step_name="testing",
        message="Testing step creation",
        status="running"
    )
    print(f"Create step result: {create_result}")
    assert create_result.get("success") == True, "Create step should succeed"
    step_id = create_result.get("data", {}).get("step_id")
    assert step_id is not None, "Step ID should be returned"
    
    # Test patch step
    print("\n4. Testing patch step...")
    patch_step_result = client.patch_step(
        execution_id="test-exec-123",
        step_id=step_id,
        status="completed",
        message="Step completed successfully"
    )
    print(f"Patch step result: {patch_step_result}")
    assert patch_step_result.get("success") == True, "Patch step should succeed"
    
    # Reset environment
    os.environ.pop('USE_MOCK_CLIENT', None)
    
    print("\n✅ Client test completed!")


def test_factory_selection():
    """Test that factory correctly selects different clients"""
    print("\nTesting Factory Client Selection...")
    
    # Test default client (HTTP client)
    os.environ.pop('USE_MOCK_CLIENT', None)
    client = create_task_manager_client()
    print(f"Default client: {type(client).__name__}")
    assert "HttpTaskManagerClient" in type(client).__name__, "Should be HTTP client"
    
    # Test mock client
    os.environ['USE_MOCK_CLIENT'] = 'true'
    client = create_task_manager_client()
    print(f"Mock client: {type(client).__name__}")
    assert "MockTaskManagerClient" in type(client).__name__, "Should be Mock client"
    
    # Reset to default
    os.environ.pop('USE_MOCK_CLIENT', None)
    
    print("✅ Factory selection test completed!")


if __name__ == "__main__":
    test_factory_selection()
    test_generated_client()

