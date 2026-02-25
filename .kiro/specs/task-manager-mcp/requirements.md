# Requirements Document

## Introduction

Nova Task Manager MCP Server is a service based on MCP (Model Context Protocol) that reports Agent execution progress to the Task Manager service. This service provides a set of tools that allow Agents to register sessions, create execution steps, update step status, and check service health.

## Glossary

- **MCP_Server**: MCP server implemented based on the fastmcp framework, providing tools for Agent invocation
- **Task_Manager**: Backend service responsible for managing tasks and execution status
- **Execution**: A task execution instance containing multiple steps
- **Step**: A single step in the execution process with status and message
- **Session_ID**: Unique identifier for an Agent session
- **Step_Status**: Step status enumeration including running, completed, failed, skipped
- **Client**: Client implementation for communicating with Task Manager
- **HTTP_Client**: Client that communicates with the real Task Manager API via HTTP protocol
- **Mock_Client**: Mock client implementation for testing
- **NOVA_EXECUTION_ID**: Environment variable containing the current execution's execution_id, which Agents can retrieve from this environment variable

## Requirements

### Requirement 1: Session Registration

**User Story:** As an Agent, I want to register my session ID at the start of execution so that Task Manager can track my execution status.

#### Acceptance Criteria

1. WHEN Agent calls the update_execution_session tool with execution_id and session_id THEN MCP_Server SHALL call the Task Manager API to update the execution's session_id
2. WHEN Task Manager API returns success THEN MCP_Server SHALL return a response containing success=True and the updated data
3. IF Task Manager API call fails THEN MCP_Server SHALL return a response containing success=False and error information
4. THE update_execution_session tool SHALL require two mandatory parameters: execution_id and session_id
5. THE update_execution_session tool description SHALL inform the Agent that execution_id can be retrieved from the NOVA_EXECUTION_ID environment variable
6. THE update_execution_session tool description SHALL inform the Agent that session_id can be obtained through the skill tool

### Requirement 2: Step Creation

**User Story:** As an Agent, I want to create execution steps to record my work progress so that users can understand the detailed execution process.

#### Acceptance Criteria

1. WHEN Agent calls the create_step tool with execution_id and step_name THEN MCP_Server SHALL create a new step
2. WHEN step creation succeeds THEN MCP_Server SHALL return a response containing step_id for subsequent updates
3. WHEN Agent provides the optional message parameter THEN MCP_Server SHALL include that message in the created step
4. WHEN Agent provides the optional status parameter THEN MCP_Server SHALL use that status as the step's initial status
5. WHEN Agent does not provide the status parameter THEN MCP_Server SHALL use "running" as the default initial status
6. THE MCP_Server SHALL only accept the following status values: running, completed, failed, skipped
7. IF Agent provides an invalid status value THEN MCP_Server SHALL return an error response containing success=False and a list of valid statuses
8. IF step creation fails THEN MCP_Server SHALL return a response containing success=False and error information
9. THE create_step tool description SHALL inform the Agent that execution_id can be retrieved from the NOVA_EXECUTION_ID environment variable

### Requirement 3: Step Update

**User Story:** As an Agent, I want to update step status and messages to reflect execution progress in real-time.

#### Acceptance Criteria

1. WHEN Agent calls the update_step tool with a valid status THEN MCP_Server SHALL update the step status
2. THE MCP_Server SHALL only accept the following status values: running, completed, failed, skipped
3. IF Agent provides an invalid status value THEN MCP_Server SHALL return an error response containing success=False and a list of valid statuses
4. IF Agent provides neither status nor message parameter THEN MCP_Server SHALL return an error indicating at least one parameter is required
5. WHEN Agent provides the message parameter THEN MCP_Server SHALL update the step's message content
6. WHEN step update succeeds THEN MCP_Server SHALL return a response containing success=True and the updated data
7. THE update_step tool description SHALL inform the Agent that execution_id can be retrieved from the NOVA_EXECUTION_ID environment variable

### Requirement 4: Health Check

**User Story:** As an operations personnel, I want to check service health status to monitor system operation.

#### Acceptance Criteria

1. WHEN user calls the health_check tool THEN MCP_Server SHALL return the health status of the Task Manager service
2. WHEN using HTTP_Client and the service is healthy THEN MCP_Server SHALL return a response containing configuration information (host, port, base_url)
3. IF Task Manager service is unavailable THEN MCP_Server SHALL return a response containing error information

### Requirement 5: Client Strategy Pattern

**User Story:** As a developer, I want to switch between real HTTP client and Mock client to develop and test in different environments.

#### Acceptance Criteria

1. THE Client_Factory SHALL select client implementation based on the USE_MOCK_CLIENT environment variable
2. WHEN USE_MOCK_CLIENT environment variable is "true" THEN Client_Factory SHALL return a Mock_Client instance
3. WHEN USE_MOCK_CLIENT environment variable is "false" or not set THEN Client_Factory SHALL return an HTTP_Client instance
4. THE HTTP_Client SHALL read configuration from environment variables: TASK_MANAGER_HOST (default localhost), TASK_MANAGER_PORT (default 8080), TASK_MANAGER_TIMEOUT (default 30 seconds)
5. THE Mock_Client SHALL maintain execution and step data in memory for test verification

### Requirement 6: HTTP Client Implementation

**User Story:** As a system integrator, I want the HTTP client to correctly call the Task Manager API to communicate with the backend service.

**Technical Note:** The project uses `openapi-python-client` to automatically generate typed API client code from `docs/swagger.yaml`. When the API definition is updated, run `make regenerate` to regenerate the client.

#### Acceptance Criteria

1. WHEN calling patch_execution THEN HTTP_Client SHALL send a PATCH request to /api/executions/{execution-id}
2. WHEN calling create_step THEN HTTP_Client SHALL send a POST request to /api/executions/{execution-id}/steps
3. WHEN calling patch_step THEN HTTP_Client SHALL send a PATCH request to /api/executions/{execution-id}/steps/{step-id}
4. WHEN calling health_check THEN HTTP_Client SHALL send a GET request to /api/health
5. IF HTTP request times out THEN HTTP_Client SHALL return a response containing "Request timeout" error
6. IF unable to connect to Task Manager THEN HTTP_Client SHALL return a response containing connection failure information
7. IF HTTP response status code >= 400 THEN HTTP_Client SHALL parse the error response and return a response containing error and error_code
8. THE project SHALL provide Makefile commands to generate client code from swagger.yaml
9. THE generated client code SHALL be located in the src/clients/generated/ directory

### Requirement 7: Data Models

**User Story:** As a developer, I want clear data model definitions to understand and use API data structures.

#### Acceptance Criteria

1. THE StepStatus enumeration SHALL define four states: running, completed, failed, skipped
2. THE ExecutionPatch data class SHALL contain optional session_id and worktree_path fields
3. THE StepCreate data class SHALL contain mandatory step_name and optional message, status fields
4. THE StepPatch data class SHALL contain optional status and message fields
