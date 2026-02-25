# Implementation Plan: Task Manager MCP

## Overview

This task list is reverse-engineered from the implemented code, primarily used to document implementation status and supplement test coverage. Since core functionality is already implemented, tasks focus on verifying existing implementation and supplementing property tests.

**Important Note:** The project uses `openapi-python-client` to automatically generate API client code from `docs/swagger.yaml`. After modifying the API definition, run `make regenerate` to regenerate client code to the `src/clients/generated/` directory.

## Tasks

- [x] 1. Data Model Implementation
  - [x] 1.1 Implement StepStatus enumeration
    - Define four states: running, completed, failed, skipped
    - _Requirements: 7.1_
  
  - [x] 1.2 Implement data classes
    - Implement ExecutionPatch, StepCreate, StepPatch data classes
    - _Requirements: 7.2, 7.3, 7.4_

- [x] 2. Client Abstraction Layer Implementation
  - [x] 2.1 Implement TaskManagerClientBase abstract base class
    - Define abstract methods: patch_execution, create_step, patch_step, health_check
    - _Requirements: 5.1_
  
  - [x] 2.2 Implement HttpTaskManagerClient
    - Implement HTTP request sending and response handling
    - Implement environment variable configuration reading
    - Note: Project uses `make regenerate` to generate typed client from swagger.yaml to src/clients/generated/
    - _Requirements: 5.4, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9_
  
  - [x] 2.3 Implement MockTaskManagerClient
    - Implement in-memory data storage
    - Implement mock API responses
    - _Requirements: 5.5_
  
  - [x] 2.4 Implement create_task_manager_client factory method
    - Select client based on USE_MOCK_CLIENT environment variable
    - _Requirements: 5.1, 5.2, 5.3_

- [x] 3. MCP Tools Implementation
  - [x] 3.1 Implement update_execution_session tool
    - Accept execution_id and session_id parameters
    - Call client patch_execution method
    - _Requirements: 1.1, 1.2, 1.3, 1.4_
  
  - [x] 3.2 Implement create_step tool
    - Accept execution_id, step_name and optional message, status parameters
    - Implement status value validation (only accept running/completed/failed/skipped)
    - Call client create_step method
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8_
  
  - [x] 3.3 Implement update_step tool
    - Accept execution_id, step_id, optional status and message parameters
    - Implement status value validation
    - Call client patch_step method
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_
  
  - [x] 3.4 Implement health_check tool
    - Call client health_check method
    - _Requirements: 4.1, 4.2, 4.3_
  
  - [x] 3.5 Update MCP tool descriptions
    - Add "can be retrieved from NOVA_EXECUTION_ID environment variable" hint in execution_id parameter description
    - Add "can be obtained through skill tool" hint in session_id parameter description
    - Update three tools: update_execution_session, create_step, update_step
    - _Requirements: 1.5, 1.6, 2.5, 3.7_

- [ ] 4. Unit Tests
  - [ ]* 4.1 Write MCP tool unit tests
    - Test parameter validation logic
    - Test error response format
    - _Requirements: 1.4, 3.2, 3.3, 3.4_
  
  - [ ]* 4.2 Write client unit tests
    - Test factory method selection logic
    - Test Mock client data management
    - _Requirements: 5.1, 5.2, 5.3, 5.5_
  
  - [ ]* 4.3 Write data model unit tests
    - Test enumeration values
    - Test data class fields
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [ ] 5. Property Tests
  - [ ]* 5.1 Write response format consistency property test
    - **Property 1: Response Format Consistency**
    - **Validates: Requirements 1.2, 1.3, 2.2, 2.4, 3.6**
  
  - [ ]* 5.2 Write status value validation property test
    - **Property 2: Status Value Validation**
    - **Validates: Requirements 3.2, 3.3**
  
  - [ ]* 5.3 Write Mock client state consistency property test
    - **Property 3: Mock Client State Consistency**
    - **Validates: Requirements 5.5**
  
  - [ ]* 5.4 Write factory method selection correctness property test
    - **Property 4: Factory Method Selection Correctness**
    - **Validates: Requirements 5.1, 5.2, 5.3**
  
  - [ ]* 5.5 Write HTTP error response handling property test
    - **Property 5: HTTP Error Response Handling**
    - **Validates: Requirements 6.7**
  
  - [ ]* 5.6 Write step creation initial status property test
    - **Property 6: Step Creation Initial Status**
    - **Validates: Requirements 2.1**
  
  - [ ]* 5.7 Write parameter passing integrity property test
    - **Property 7: Parameter Passing Integrity**
    - **Validates: Requirements 1.1, 2.3, 3.1, 3.5**

- [ ] 6. Checkpoint - Ensure all tests pass
  - Run all tests, consult user if there are issues

## Notes

- Tasks marked with `[x]` indicate they are already implemented in existing code
- Tasks marked with `*` are optional tasks that can be skipped to accelerate MVP progress
- Each task references specific requirements for traceability
- Property tests verify general correctness properties
- Unit tests verify specific examples and boundary conditions
