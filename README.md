# Trello MCP Server

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

#### Pulling the Docker Image (Alternative to Building)

- A pre-built image is available at Docker Hub and is updated automatically by CI:

```bash
docker pull valerok86/trello-mcp-server:latest
```

Then run it with your `.env` file mounted:

```bash
docker run --env-file .env -p 8000:8000 valerok86/trello-mcp-server:latest
```

##### How to Prepare Your `.env` File

1. **Get the Example File:**
   - In the root of this repository, you will find a file named `.env.example`.
   - Download or copy this file to your working directory and rename it to `.env`:
     ```bash
     cp .env.example .env
     ```

2. **Edit the `.env` File:**
   - Open `.env` in your favorite text editor.
   - Fill in the required values. At minimum, you need:
     ```env
     TRELLO_API_KEY=your_trello_api_key_here
     TRELLO_TOKEN=your_trello_token_here
     USE_CLAUDE_APP=false
     MCP_SERVER_HOST=0.0.0.0
     MCP_SERVER_PORT=8000
     ```
   - You can get your Trello API key and token by following the instructions in the "Installation" section above.
   - **Tip:** Never commit your `.env` file to a public repository, as it contains sensitive credentials.

3. **Where to Place the `.env` File:**
   - Place the `.env` file in the same directory where you run your `docker run` command.
   - Example directory structure:
     ```
     /your/project/
       ├── .env
       └── (other files)
     ```

4. **Full Example Workflow:**
   ```bash
   # Clone the repository (optional, for getting the .env.example file)
   git clone https://github.com/m0xai/trello-mcp-server.git
   cd trello-mcp-server

   # Copy and edit the .env file
   cp .env.example .env
   # (edit .env with your credentials)

   # Pull and run the Docker image
   docker pull valerok86/trello-mcp-server:latest
   docker run --env-file .env -p 8000:8000 valerok86/trello-mcp-server:latest
   ```

This allows you to get started quickly without building the image locally.

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

## Trello API Rate Limiting

This server automatically handles Trello API rate limits as described in the [official Trello documentation](https://developer.atlassian.com/cloud/trello/guides/rest-api/rate-limits/):

- Trello enforces a limit of 300 requests per 10 seconds per API key, and 100 requests per 10 seconds per token.
- If a rate limit is exceeded, Trello returns a 429 error and may include a `Retry-After` header.
- The MCP server's Trello API client will automatically detect 429 errors, wait for the appropriate time (using the `Retry-After` header if present, otherwise using exponential backoff), and retry the request up to 5 times.
- This ensures your requests are less likely to fail due to rate limiting, and you do not need to implement this logic yourself.

**Reference:** [Trello API Rate Limits](https://developer.atlassian.com/cloud/trello/guides/rest-api/rate-limits/)

## Client Integration

### Using with Claude Desktop

1. Run the server in Claude app mode (`USE_CLAUDE_APP=true`)
2. Start or restart Claude Desktop
3. Claude will automatically detect and connect to your MCP server

### Using with Cursor

To connect your MCP server to Cursor:

1. Run the server in SSE mode (`USE_CLAUDE_APP=false`)
2. In Cursor, go to Settings (gear icon) > AI > Model Context Protocol
3. Add a new server with URL `http://localhost:8000` (or your configured host/port), alternative to use dokcer 127.0.0.1 (not exposed to the outside work) and in the scp configuraiton use "url": `http://host.docker.internal:8952/sse`
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

### Automatic Trello Authorization URL

If the server encounters a 401 Unauthorized error when communicating with the Trello API, it will automatically log a URL that you can visit to authorize the app for your Trello account. This URL is generated using your API key from the `.env` file and looks like this:

```
https://trello.com/1/authorize?expiration=never&name=Trello+Assistant+MCP&scope=read,write&response_type=token&key=<YOUR_API_KEY>
```

**How to use:**
1. Copy the URL from the server logs when prompted.
2. Open it in your browser and approve the app.
3. Copy the generated token and update your `.env` file as `TRELLO_TOKEN=your_new_token`.
4. Restart the server to apply the new token.

This makes it easy to authorize the app for any Trello user without manual URL construction.

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
- ✅ Read all cards in a list (with optional filtering by creation or last activity date using the `from_date` parameter)
- ✅ Read specific card details
- ✅ Create new cards
- ✅ Update card attributes
- ✅ Move cards between lists (columns) using the new `move_card` endpoint/tool
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
- "Show me all cards in list [list_name] created or updated since 2025-01-01"
- "Move card [card_name] to the [target_list_name] column"

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

## Automatic Trello Authorization URL

If the server encounters a 401 Unauthorized error when communicating with the Trello API, it will automatically log a URL that you can visit to authorize the app for your Trello account. This URL is generated using your API key from the `.env` file and looks like this:

```
https://trello.com/1/authorize?expiration=never&name=Trello+Assistant+MCP&scope=read,write&response_type=token&key=<YOUR_API_KEY>
```

**How to use:**
1. Copy the URL from the server logs when prompted.
2. Open it in your browser and approve the app.
3. Copy the generated token and update your `.env` file as `TRELLO_TOKEN=your_new_token`.
4. Restart the server to apply the new token.

This makes it easy to authorize the app for any Trello user without manual URL construction.

## Trello Open API documnetation
```
https://developer.atlassian.com/cloud/trello/rest/api-group-cards/#api-cards-post 
```