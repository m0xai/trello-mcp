# Trello MCP Server

A powerful MCP server for interacting with Trello boards, lists, and cards via AI Hosts.

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Prerequisites](#prerequisites)
- [Pre-installation](#pre-installation)
- [Installation](#installation)
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

## Capabilities

| Operation | Board | List | Card |
|-----------|-------|------|------|
| Read      | ✅    | ✅    | ✅   |
| Write     | ❌    | ✅    | ✅   |
| Update    | ❌    | ✅    | ✅   |
| Delete    | ❌    | ✅    | ✅   |

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


## Troubleshooting

If you encounter issues:

1. Verify your Trello API credentials in the `.env` file
2. Check that you have proper permissions in your Trello workspace
3. Ensure Claude for Desktop is running the latest version
4. Check the logs for any error messages with `uv run mcp dev main.py` command.
5. Make sure uv is properly installed and in your PATH

## Contributing

Feel free to submit issues and enhancement requests!
