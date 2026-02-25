---
inclusion: always
---

# Task Manager MCP Project Conventions

## Code Generation

**Important:** The API client code in this project is auto-generated. Do not manually modify generated files.

### Client Code Generation

- **Generation Tool**: `openapi-python-client`
- **Source File**: `docs/swagger.yaml`
- **Output Directory**: `src/clients/generated/`
- **Generation Commands**: 
  - `make regenerate` - Clean and regenerate client
  - `make generate` - Generate client only
  - `make clean` - Clean generated code

### Workflow

1. Modify API definition in `docs/swagger.yaml`
2. Run `make regenerate` to regenerate client code
3. Update hand-written wrapper code (e.g., `src/clients/http_client.py`) to use new API
4. Run tests to verify changes

**Note**: Generated code is located in `src/clients/generated/_client/` directory, including:
- `api/` - API endpoint functions
- `models/` - Data model classes
- `client.py` - Client base class

## Git Commit Conventions

### Pre-commit Hook

The project has a pre-commit hook configured that automatically runs tests before each commit:

```bash
# Hook location
.git/hooks/pre-commit

# Automatically executes
make test
```

If tests fail, the commit will be blocked. Fix the tests and try committing again.

**Skip hook (not recommended)**:
```bash
git commit --no-verify -m "your message"
```

### Commit Message Format

Use concise one-line format following Conventional Commits specification:

```
<type>: <description>
```

### Type Categories

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation update
- `style`: Code formatting (no functional changes)
- `refactor`: Code refactoring
- `test`: Add or modify tests
- `chore`: Build tools, dependency updates, etc.

### Examples

```bash
feat: add status parameter to create_step API
fix: handle timeout error in HTTP client
docs: update API usage examples in README
chore: regenerate client from updated swagger spec
refactor: simplify error handling in MCP tools
test: add property tests for step creation
```

### Rules

- Use English descriptions
- Start with lowercase
- Do not end with period
- Description should be clear and concise, explaining what was changed
- One commit should do one thing

## Project Structure

```
.
├── docs/
│   └── swagger.yaml          # API definition (source file)
├── src/
│   ├── clients/
│   │   ├── generated/        # Auto-generated client (do not modify manually)
│   │   ├── base_client.py    # Client abstract base class
│   │   ├── http_client.py    # HTTP client implementation
│   │   ├── mock_client.py    # Mock client implementation
│   │   └── client_factory.py # Client factory
│   ├── models/               # Data models
│   └── server/               # MCP server
├── tests/                    # Test files
├── Makefile                  # Build and generation commands
└── .kiro/
    ├── specs/                # Feature specification documents
    └── steering/             # Project conventions and guidelines
```
