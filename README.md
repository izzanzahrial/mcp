# MCP Server
## Create virtual environment and activate it
```bash
uv venv
source .venv/bin/activate
```

## Install dependencies
```bash
uv add "mcp[cli]" httpx
```

## To launch it by running 
```bash
uv --directory /ABSOLUTE/PATH/TO/PARENT/FOLDER/mcp run mcp.py
```

## Create .env file
```bash
touch .env
```

## Add your key to the .env file:
```.env
ANTHROPIC_API_KEY=<your_key_here>
```

# MCP Client
## To run your client with any MCP server:
```bash
uv run client.py path/to/server.py # python server
uv run client.py path/to/build/index.js # node server
```

## Relative path
```bash
uv run client.py ./server/weather.py
```

## Absolute path
```bash
uv run client.py /Users/username/projects/mcp-server/weather.py
```

## Windows path (either format works)
```bash
uv run client.py C:/projects/mcp-server/weather.py
uv run client.py C:\\projects\\mcp-server\\weather.py
```