# Task Manager MCP

Nova Agent progress reporting MCP server.

## Installation

### Method 1: Docker Installation (Recommended)

#### 1. Build Docker Image

```bash
./build-docker.sh
```

#### 2. Add to Claude Desktop

**macOS/Windows:**

```bash
claude mcp add task-manager -s user \
  --env "TASK_MANAGER_HOST=host.docker.internal" \
  --env "TASK_MANAGER_PORT=8080" \
  --env "TASK_MANAGER_TIMEOUT=30" \
  --env "USE_MOCK_CLIENT=false" \
  -- docker run -i --rm \
    -e TASK_MANAGER_HOST \
    -e TASK_MANAGER_PORT \
    -e TASK_MANAGER_TIMEOUT \
    -e USE_MOCK_CLIENT \
    task-manager-mcp:latest
```

**Linux:**

```bash
claude mcp add task-manager -s user \
  --env "TASK_MANAGER_HOST=localhost" \
  --env "TASK_MANAGER_PORT=8080" \
  --env "TASK_MANAGER_TIMEOUT=30" \
  --env "USE_MOCK_CLIENT=false" \
  -- docker run -i --rm --network=host \
    -e TASK_MANAGER_HOST \
    -e TASK_MANAGER_PORT \
    -e TASK_MANAGER_TIMEOUT \
    -e USE_MOCK_CLIENT \
    task-manager-mcp:latest
```

**Mock Mode (for testing):**

```bash
claude mcp add task-manager-mock -s user \
  --env "USE_MOCK_CLIENT=true" \
  -- docker run -i --rm \
    -e USE_MOCK_CLIENT \
    task-manager-mcp:latest
```

### Method 2: Local Python Installation

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2. Manual MCP Configuration

Edit Claude Desktop's MCP configuration file (refer to `mcp-config-example.json`):

```json
{
  "mcpServers": {
    "task-manager": {
      "command": "python3",
      "args": ["/path/to/your/task_manager_mcp.py"],
      "env": {
        "TASK_MANAGER_HOST": "localhost",
        "TASK_MANAGER_PORT": "8080",
        "TASK_MANAGER_TIMEOUT": "30",
        "USE_MOCK_CLIENT": "false"
      }
    }
  }
}
```

### Uninstallation

```bash
# Remove MCP server
claude mcp remove task-manager

# Or remove mock version
claude mcp remove task-manager-mock
```

## MCP Tools

| Tool | Purpose |
|------|---------|
| `update_execution_session` | Update execution's session_id |
| `create_step` | Create a step and return step_id |
| `update_step` | Update step status/message |
| `health_check` | Health check |

## Usage Example

```python
# 1. Register session
update_execution_session(execution_id="exec-123", session_id="nova-001")

# 2. Create step
result = create_step(execution_id="exec-123", step_name="analyzing")
step_id = result["step_id"]

# 3. Complete step
update_step(execution_id="exec-123", step_id=step_id, status="completed")
```

## Step Status

- `running` - In progress
- `completed` - Completed
- `failed` - Failed
- `skipped` - Skipped

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TASK_MANAGER_HOST` | Task Manager service address | `localhost` |
| `TASK_MANAGER_PORT` | Task Manager service port | `8080` |
| `TASK_MANAGER_TIMEOUT` | Request timeout (seconds) | `30` |
| `USE_MOCK_CLIENT` | Whether to use Mock client | `false` |

### Docker Network Notes

- **macOS/Windows**: Use `host.docker.internal` to access host services
- **Linux**: Use `--network=host` and `localhost` to access host services

## Development

### Run Locally

```bash
pip install -r requirements.txt
python task_manager_mcp.py
```

### Run Tests

```bash
make test
# or
python tests/simple_test.py
python tests/test_generated_client.py
```

## Error Handling

When backend API is unavailable, MCP returns clear error messages:

**404 Error (API not implemented):**
```json
{
  "success": false,
  "error": "API endpoint not found: PATCH /api/executions/{id}/steps/{step_id}. The backend service may not have implemented this API yet.",
  "status_code": 404,
  "hint": "Please check if the Task Manager backend service has this endpoint implemented."
}
```

**Connection Failed:**
```json
{
  "success": false,
  "error": "Cannot connect to Task Manager service at http://localhost:8080",
  "hint": "Please verify that the Task Manager service is running and the host/port are correct."
}
```
