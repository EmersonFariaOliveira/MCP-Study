
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from dotenv import load_dotenv
load_dotenv()


client = MultiServerMCPClient(
	{
		"Math": {
			"transport": "stdio",  # Local subprocess communication
			"command": "python",
			# Relative path to your math_server.py file
			"args": ["../MCP-Server/math_server.py"],
		},
		"weather": {
			"transport": "stdio",
			"command": "python",
			# Relative path to your weather_server.py file
			"args": ["../MCP-Server/weather_server.py"],
		},
	}
)


async def main():
	"""Entry point: asynchronous to allow awaiting client.get_tools().

	This avoids the "await allowed only within async function" error by
	moving awaits inside an async function and using asyncio.run at the
	module entrypoint.
	"""
	tools = await client.get_tools()

	agent = create_agent(
		# "anthropic:claude-sonnet-4-5",
		"gpt-4o",
		tools  
	)

	# math_response = await agent.ainvoke(
	# 	{"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
	# )
	# print("math_response")
	# print(math_response)

	weather_response = await agent.ainvoke(
		{"messages": [{"role": "user", "content": "what is the weather in nyc?"}]}
	)

	print("weather_response")
	print(weather_response)

if __name__ == "__main__":
	asyncio.run(main())


