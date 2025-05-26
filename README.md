# MCP Server
1. Create virtual environment and activate it

    ```bash
    uv venv
    source .venv/bin/activate
    ```

2. Install dependencies
    ```bash
    uv add mcp httpx arxiv
    ```

3. To launch it by running 
    ```bash
    uv --directory /ABSOLUTE/PATH/TO/PARENT/FOLDER/mcp run server.py
    ```

4. Create .env file
    ```bash
    touch .env
    ```

5. Add your key to the .env file:
    ```.env
    ANTHROPIC_API_KEY=<your_key_here>
    ```

6. To test your MCP Server you can use mcp inspector
    ```bash
    npx @modelcontextprotocol/inspector uv run server.py
    ```

# MCP Client
1. Install required packages
    ```bash
    uv add mcp anthropic python-dotenv nest_asyncio
    ```

2. To run your client with any MCP server:
    ```bash
    uv run client.py path/to/server.py # python server
    uv run client.py path/to/build/index.js # node server
    ```
    Relative path
    ```bash
    uv run client.py ./server/server.py
    ```
    Absolute path
    ```bash
    uv run client.py /Users/username/projects/mcp/server.py
    ```
    
    Windows path (either format works)
    ```bash
    uv run client.py C:/projects/mcp/server.py
    uv run client.py C:\\projects\\mcp\\server.py
    ```

# Deployment
1. If the server using pip instead of uv
    ```bash
    uv pip compile pyproject.toml > requirements.txt
    ``` 

2. Make sure the server use the right python version
    ```bash
    echo "python-3.11.11" > runtime.txt
    ```

3. Input the required environment variables

4. Run the mcp server
    ```bash
    python server.py
    ```

references :
- https://www.youtube.com/watch?v=wa_A0qY0anA
- https://learn.deeplearning.ai/courses/mcp-build-rich-context-ai-apps-with-anthropic/lesson/fkbhh/introduction