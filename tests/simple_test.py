#!/usr/bin/env python3
"""
Simple tests for MCP client functionality
"""

import os
import sys

os.environ['USE_MOCK_CLIENT'] = 'true'
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.clients import create_task_manager_client

client = create_task_manager_client()


def test_health_check():
    result = client.health_check()
    assert result["success"] is True
    print("✓ health_check")


def test_patch_execution():
    result = client.patch_execution(
        execution_id="exec-123",
        session_id="session-abc"
    )
    assert result["success"] is True
    assert result["data"]["session_id"] == "session-abc"
    print("✓ patch_execution")


def test_create_and_update_step():
    result = client.create_step(
        execution_id="exec-123",
        step_name="analyzing",
        message="Analyzing codebase"
    )
    assert result["success"] is True
    assert result["data"]["status"] == "running"
    print("✓ create_step")
    
    step_id = result["data"]["step_id"]
    
    result = client.patch_step(
        execution_id="exec-123",
        step_id=step_id,
        status="completed",
        message="Done"
    )
    assert result["success"] is True
    assert result["data"]["status"] == "completed"
    print("✓ patch_step")


def test_workflow():
    print("\n--- Workflow ---")
    
    client.patch_execution("exec-wf", "nova-001")
    print("  1. Session registered")
    
    r = client.create_step("exec-wf", "analyzing", "Starting")
    step1 = r["data"]["step_id"]
    print(f"  2. Step: {step1}")
    
    client.patch_step("exec-wf", step1, "completed", "Done")
    print("  3. Completed")
    
    r = client.create_step("exec-wf", "coding")
    step2 = r["data"]["step_id"]
    client.patch_step("exec-wf", step2, "completed")
    print("  4. Coding done")
    
    print("✓ workflow\n")


if __name__ == "__main__":
    print("Running tests...\n")
    test_health_check()
    test_patch_execution()
    test_create_and_update_step()
    test_workflow()
    print("✅ All passed!")
