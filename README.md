# Trello MCP Server

[![smithery badge](https://smithery.ai/badge/@m0xai/trello-mcp-server)](https://smithery.ai/server/@m0xai/trello-mcp-server)

A powerful MCP server for interacting with Trello boards, lists, and cards via AI Hosts.

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Prerequisites](#prerequisites)
- [Pre-installation](#pre-installation)
- [Installation](#installation)
- [Server Modes](#server-modes)
- [Configuration](#configuration)
- [Client Integration](#client-integration)
- [Capabilities](#capabilities)
- [Detailed Capabilities](#detailed-capabilities)
    - [Board Operations](#board-operations)
    - [List Operations](#list-operations)
    - [Card Operations](#card-operations)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)


## Prerequisites

1. Python 3.12 or higher, can easly managed by `uv`
2. [Claude for Desktop](https://claude.ai/download) installed
3. Trello account and API credentials
4. [uv](https://github.com/astral-sh/uv) package manager installed

## Pre-installation
1. Make sure you have installed Claude Desktop App
2. Make sure you have already logged in with your account into Claude.
3. Start Claude

## Installation

### Installing via Smithery

To install Trello MCP Server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@m0xai/trello-mcp-server):

```bash
npx -y @smithery/cli install @m0xai/trello-mcp-server --client claude
```

### Installing Manually

1. Set up Trello API credentials:
   - Go to [Trello Apps Administration](https://trello.com/power-ups/admin)
   - Create a new integration at [New Power-Up or Integration](https://trello.com/power-ups/admin/new)
   - Fill in your information (you can leave the Iframe connector URL empty) and make sure to select the correct Workspace
   - Click your app's icon and navigate to "API key" from left sidebar. 
   - Copy your "API key" and on the right side: "you can manually generate a Token." click the word token to get your Trello Token.

2. Rename the `.env.example` file in the project root with `.env` and set vairables you just got:
```bash
TRELLO_API_KEY=your_api_key_here
TRELLO_TOKEN=your_token_here
```

3. Install uv if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

4. Clone this repository:
```bash
git clone https://github.com/m0xai/trello-mcp-server.git
cd trello-mcp-server
```

5. Install dependencies and set server for Claude using uv::
```bash
uv run mcp install main.py
```

6. Restart Claude Desktop app

## Server Modes

This MCP server can run in two different modes:

### Claude App Mode

This mode integrates directly with the Claude Desktop application:

1. Set `USE_CLAUDE_APP=true` in your `.env` file (this is the default)
2. Run the server with:
```bash
uv run mcp install main.py
```
3. Restart the Claude Desktop application

### SSE Server Mode

This mode runs as a standalone SSE server that can be used with any MCP-compatible client, including Cursor:

1. Set `USE_CLAUDE_APP=false` in your `.env` file
2. Run the server with:
```bash
python main.py
```
3. The server will be available at `http://localhost:8000` by default (or your configured port)

### Docker Mode

You can also run the server using Docker Compose:

1. Make sure you have Docker and Docker Compose installed
2. Create your `.env` file with your configuration
3. Build and start the container:
```bash
docker-compose up -d
```
4. The server will run in SSE mode by default
5. To view logs:
```bash
docker-compose logs -f
```
6. To stop the server:
```bash
docker-compose down
```

## Configuration

The server can be configured using environment variables in the `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| TRELLO_API_KEY | Your Trello API key | Required |
| TRELLO_TOKEN | Your Trello API token | Required |
| MCP_SERVER_NAME | The name of the MCP server | Trello MCP Server |
| MCP_SERVER_HOST | Host address for SSE mode | 0.0.0.0 |
| MCP_SERVER_PORT | Port for SSE mode | 8000 |
| USE_CLAUDE_APP | Whether to use Claude app mode | true |

You can customize the server by editing these values in your `.env` file.

## Client Integration

### Using with Claude Desktop

1. Run the server in Claude app mode (`USE_CLAUDE_APP=true`)
2. Start or restart Claude Desktop
3. Claude will automatically detect and connect to your MCP server

### Using with Cursor

To connect your MCP server to Cursor:

1. Run the server in SSE mode (`USE_CLAUDE_APP=false`)
2. In Cursor, go to Settings (gear icon) > AI > Model Context Protocol
3. Add a new server with URL `http://localhost:8000` (or your configured host/port)
4. Select the server when using Cursor's AI features

You can also add this configuration to your Cursor settings JSON file (typically at `~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "trello": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

### Using with Other MCP Clients

For other MCP-compatible clients, point them to the SSE endpoint at `http://localhost:8000`.

### Minimal Client Example

Here's a minimal Python example to connect to the SSE endpoint:

```python
import asyncio
import httpx

async def connect_to_mcp_server():
    url = "http://localhost:8000/sse"
    headers = {"Accept": "text/event-stream"}
    
    async with httpx.AsyncClient() as client:
        async with client.stream("GET", url, headers=headers) as response:
            # Get the session ID from the first SSE message
            session_id = None
            async for line in response.aiter_lines():
                if line.startswith("data:"):
                    data = line[5:].strip()
                    if "session_id=" in data and not session_id:
                        session_id = data.split("session_id=")[1]
                        
                        # Send a message using the session ID
                        message_url = f"http://localhost:8000/messages/?session_id={session_id}"
                        message = {
                            "role": "user",
                            "content": {
                                "type": "text",
                                "text": "Show me my Trello boards"
                            }
                        }
                        await client.post(message_url, json=message)

if __name__ == "__main__":
    asyncio.run(connect_to_mcp_server())
```

## Capabilities

| Operation | Board | List | Card | Checklist | Checklist Item |
|-----------|-------|------|------|-----------|----------------|
| Read      | ✅    | ✅    | ✅   | ✅        | ✅              |
| Write     | ❌    | ✅    | ✅   | ✅        | ✅              |
| Update    | ❌    | ✅    | ✅   | ✅        | ✅              |
| Delete    | ❌    | ✅    | ✅   | ✅        | ✅              |

### Detailed Capabilities

#### Board Operations
- ✅ Read all boards
- ✅ Read specific board details

#### List Operations
- ✅ Read all lists in a board
- ✅ Read specific list details
- ✅ Create new lists
- ✅ Update list name
- ✅ Archive (delete) lists

#### Card Operations
- ✅ Read all cards in a list
- ✅ Read specific card details
- ✅ Create new cards
- ✅ Update card attributes
- ✅ Delete cards

#### Checklist Operations
- ✅ Get a specific checklist
- ✅ List all checklists in a card
- ✅ Create a new checklist
- ✅ Update a checklist
- ✅ Delete a checklist
- ✅ Add checkitem to checklist
- ✅ Update checkitem
- ✅ Delete checkitem

## Usage

Once installed, you can interact with your Trello boards through Claude. Here are some example queries:

- "Show me all my boards"
- "What lists are in board [board_name]?"
- "Create a new card in list [list_name] with title [title]"
- "Update the description of card [card_name]"
- "Archive the list [list_name]"

Here are my example usages:

<img width="1277" alt="Example Usage of Trello MCP server: Asking to list all my cards in Guitar Board" src="https://github.com/user-attachments/assets/fef29dfc-04b2-4af9-92a6-f8db2320c860" />

<img width="1274" alt="Asking to add new song card into my project songs" src="https://github.com/user-attachments/assets/2d8406ca-1dde-41c0-a035-86d5271dd78f" />

<img width="1632" alt="Asking to add new card with checklist in it" src="https://github.com/user-attachments/assets/5a63f107-d135-402d-ab33-b9bf13eca751" />

## Troubleshooting

If you encounter issues:

1. Verify your Trello API credentials in the `.env` file
2. Check that you have proper permissions in your Trello workspace
3. Ensure Claude for Desktop is running the latest version
4. Check the logs for any error messages with `uv run mcp dev main.py` command.
5. Make sure uv is properly installed and in your PATH

## Contributing

Feel free to submit issues and enhancement requests!
