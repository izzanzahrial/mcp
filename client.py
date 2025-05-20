import asyncio
from typing import Optional, List
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from anthropic import Anthropic
from dotenv import load_dotenv
import nest_asyncio

nest_asyncio.apply()

load_dotenv()  # load environment variables from .env

class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic()
        self.available_tools: List[dict] = []
    # methods will go here

    async def process_query(self, query: str):
        """Process a query using Claude and available tools"""
        messages = [
            {
                "role": "user",
                "content": query
            }
        ]

        # Initial Claude API call
        response = self.anthropic.messages.create(max_tokens = 2024,
                                        model = 'claude-3-7-sonnet-20250219', 
                                        tools = self.available_tools, # tools exposed to the LLM
                                        messages = messages)

        # Process response and handle tool calls
        process_query = True
        while process_query:
            assistant_content = []
            for content in response.content:
                if content.type =='text':
                    print(content.text)
                    assistant_content.append(content)
                    if(len(response.content) == 1):
                        process_query= False
                elif content.type == 'tool_use':
                        assistant_content.append(content)
                        messages.append({'role':'assistant', 'content':assistant_content})
                        tool_id = content.id
                        tool_args = content.input
                        tool_name = content.name
        
                        print(f"Calling tool {tool_name} with args {tool_args}")
                        
                        # Call a tool
                        #result = execute_tool(tool_name, tool_args): not anymore needed
                        # tool invocation through the client session
                        result = await self.session.call_tool(tool_name, arguments=tool_args)
                        messages.append({"role": "user", 
                                        "content": [
                                            {
                                                "type": "tool_result",
                                                "tool_use_id":tool_id,
                                                "content": result.content
                                            }
                                        ]
                                        })
                        response = self.anthropic.messages.create(max_tokens = 2024,
                                        model = 'claude-3-7-sonnet-20250219', 
                                        tools = self.available_tools,
                                        messages = messages) 
                        
                        if(len(response.content) == 1 and response.content[0].type == "text"):
                            print(response.content[0].text)
                            process_query= False
    
    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server

        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )
        async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    self.session = session
                    # Initialize the connection
                    await session.initialize()
        
                    # List available tools
                    response = await session.list_tools()
                    
                    tools = response.tools
                    print("\nConnected to server with tools:", [tool.name for tool in tools])
                    
                    self.available_tools = [{
                        "name": tool.name,
                        "description": tool.description,
                        "input_schema": tool.inputSchema
                    } for tool in response.tools]
        
                    await self.chat_loop()

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == 'quit':
                    break

                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()