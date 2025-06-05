# Trello MCP Server

A powerful MCP server for interacting with Trello boards, lists, and cards via AI Hosts.
It was designed for use with **Claude Desktop**, but also supports other clients via **SSE server mode**.

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

### Claude Desktop mode

- [Claude for Desktop](https://claude.ai/download) installed
- You have already logged in with your account into Claude
- A git client, so you can clone this repository
- [uv](https://docs.astral.sh/uv/#installation) to run python. It manages python versions and dependencies too.
- Trello account, so you can get API credentials (later in this guide)

### SSE server mode

- A git client, so you can clone this repository
- [Docker](https://www.docker.com/) to run the server with docker
- or [uv](https://docs.astral.sh/uv/#installation) to run the server with python if you donøt want to use docker

## Installation for Claude Desktop mode

First, set up Trello API credentials:

- Go to [Trello Apps Administration](https://trello.com/power-ups/admin)
- Create a new integration at [New Power-Up or Integration](https://trello.com/power-ups/admin/new)
- Fill in your information (you can leave the Iframe connector URL empty) and make sure to select the correct Workspace
- Click your app's icon and navigate to "API key" from left sidebar
    - **NOTE**: The secret you see on that screen is **NOT** your token
- Copy your "API key" and store it safely, you will need it later
- On the right side, hidden in the text: "you can manually generate a Token." 
    - Click the word "Token" to get af form to fill out for your Trello Token 
- Fill out the form and then click next

- You will now get your Token. Store it safely, you will need it later


Then, clone this repository:

```bash
git clone https://github.com/m0xai/trello-mcp-server.git
cd trello-mcp-server
```

Then, Rename the `.env.example` file in the project root with `.env` and set the TRELLO_... variables you just got:

```bash
TRELLO_API_KEY=your_api_key_here
TRELLO_TOKEN=your_token_here
```

Then, Install uv if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Then, use uv to get pythonm install dependencies and install the server for Claude using uv:
```bash
uv run mcp install main.py
```

Finally, **restart** Claude Desktop app.
It should be ready to use. Try asking it to summarize a Trello card.


## Installation for SSE server mode

This mode runs as a standalone SSE server that can be used with any MCP-compatible client, including Cursor.
The server will be available at `http://localhost:8000/sse` by default (or change the port by modifying MCP_SERVER_PORT in your .env file)

You can run with docker or python (using uv)

### Run with Docker

You can choose to run with Docker (then you don't need python and uv)), if you run this command: 

```bash
docker compose up -d
```

To view logs:

```bash
docker compose logs -f
```

To stop the server:

```bash
docker compose down
```

### Run with Python and 'uv'

As an alternative, you can choose to run with python (then you don't need docker)), if you run this command: 

```bash
USE_CLAUDE_APP=false uv run main.py
```

### Client Integration for SSE mode, Using with Cursor

To connect your MCP server to Cursor:
2. In Cursor, go to Settings (gear icon) > AI > Model Context Protocol
3. Add a new server with URL `http://localhost:8000/sse` (or your configured host/port)
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

For other MCP-compatible clients, point them to the SSE endpoint at `http://localhost:8000/sse`.

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
