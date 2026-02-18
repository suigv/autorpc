# AutoRPC - MYT RPA 自动化控制系统

Multi-mode RPA automation control system for social media operations.

## Features

- **GUI Desktop App** - Tkinter-based visual interface
- **REST API** - HTTP API for programmatic control
- **MCP Server** - AI model integration (Claude, GPT, etc.)
- **OpenCode Skills** - Natural language task triggering

## Support

| Mode | Description |
|------|-------------|
| GUI | Tkinter desktop application |
| API | FastAPI REST service |
| Skills | OpenCode natural language |
| MCP | AI model tool integration |

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Set your AI provider API keys via environment variables:

```bash
export VOLC_API_KEY="your_volc_api_key"
export PART_TIME_API_KEY="your_part_time_api_key"
```

### 3. Start Services

```bash
# GUI Mode (original)
python main.py

# API Mode
uvicorn app.main:app --host 0.0.0.0 --port 8000

# MCP Mode (requires API first)
python3 mcp_server.py
```

## API Usage

```bash
# Get config
curl http://localhost:8000/api/config/

# Start full flow
curl -X POST http://localhost:8000/api/tasks/full-flow \
  -H "Content-Type: application/json" \
  -d '{"devices": [1,2,3], "ai_type": "volc"}'

# Batch start
curl -X POST "http://localhost:8000/api/devices/batch/start?devices=1-5&task_type=nurture_flow"
```

## Task Types

| Type | Description |
|------|-------------|
| full_flow | Full automation (reset → login → scrape → clone → follow → nurture loop) |
| nurture_flow | Nurture loop (scrape → nurture → DM reply) |
| reset_login | Reset device and login |

## AI Providers

Support for custom AI providers via `common/ai_providers.py`:

- Volcano Engine (豆包大模型)
- Custom providers can be added

## Project Structure

```
├── app/              # FastAPI application
│   ├── api/         # API routes
│   ├── core/        # Core services
│   └── models/      # Pydantic models
├── common/          # Shared modules
├── tasks/           # Task implementations
├── skills/          # Python module (legacy)
├── mcp_server.py    # MCP server
├── main.py          # GUI application
└── config/          # Configuration
```

## License

MIT
