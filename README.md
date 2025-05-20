# Create virtual environment and activate it
uv venv
source .venv/bin/activate

# Install dependencies
uv add "mcp[cli]" httpx

# To launch it by running 
uv --directory /ABSOLUTE/PATH/TO/PARENT/FOLDER/mcp run mcp.py