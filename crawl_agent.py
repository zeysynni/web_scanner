import openai
from contextlib import AsyncExitStack
from agents.mcp import MCPServerStdio
from agents import Agent, Tool, Runner, trace, RunConfig, ModelSettings
from agents.models.openai_provider import OpenAIProvider


from mcp_params import web_crawling_mcp_params
from prompts import scanner_instruction
#from webpage_structure import Webpages
from webpage_structure import Webpages
from utils import *

# defines the mcp_server and agent for web crawling
# defines also the launch function for crawler

async def create_mcp_servers(stack: AsyncExitStack):
    web_servers = [
        await stack.enter_async_context(
            MCPServerStdio(
                params,
                client_session_timeout_seconds=120
            )
        )
        for params in web_crawling_mcp_params
    ]
    return web_servers

async def create_craw_agent(stack: AsyncExitStack) -> Agent:
    craw_server= await create_mcp_servers(stack)
    agent = Agent(
        name="crawler", 
        instructions=scanner_instruction, 
        model="gpt-4.1-mini", 
        mcp_servers=craw_server,
        output_type=Webpages,
    )
    return agent

async def launch_crawler(agent, topic, message):
    openai_client = openai.AsyncOpenAI(
        max_retries=5,  # retry up to 5 times
    )
    run_config = RunConfig(
        model_provider=OpenAIProvider(openai_client=openai_client),
        model_settings=ModelSettings(
            temperature=0,
            )
    )
    with trace(f"{topic}"):
        result = await Runner.run(agent, message, max_turns=200, run_config=run_config)

    path = save_json(result, filename=topic)
    print(path)