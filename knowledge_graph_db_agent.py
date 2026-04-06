from ast import Str
from contextlib import AsyncExitStack
import openai

from agents.mcp import MCPServerStdio
from agents import Agent, Tool, Runner, trace, RunConfig, ModelSettings
from agents.models.openai_provider import OpenAIProvider

async def create_db_servers(stack: AsyncExitStack, db_params: list):
    # could be easily extended if more mcp servers are needed
    db_servers = [
        await stack.enter_async_context(
            MCPServerStdio(
                params,
                client_session_timeout_seconds=30
            )
        )
        for params in db_params
    ]
    return db_servers

async def create_db_agent(stack: AsyncExitStack, ingest_instruction: str, db_params: list) -> Agent:
    db_server = await create_db_servers(stack, db_params)
    agent = Agent(
        name="Databank", 
        instructions=ingest_instruction, 
        model="gpt-4.1-mini", 
        mcp_servers=db_server,
    )
    return agent

async def create_faq_agent(stack: AsyncExitStack, qa_instruction: str, db_params: list) -> Agent:
    db_server = await create_db_servers(stack, db_params)
    agent = Agent(
        name="FAQ", 
        instructions=qa_instruction, 
        model="gpt-4.1-mini", 
        mcp_servers=db_server,
    )
    return agent

async def launch_DB(agent, topic, message):
    openai_client = openai.AsyncOpenAI(
        max_retries=5,  # retry up to 5 times
    )
    run_config = RunConfig(
        model_provider=OpenAIProvider(openai_client=openai_client),
        model_settings=ModelSettings(temperature=0),
    )
    with trace(f"{topic}_db"):
        result = await Runner.run(agent, input=message, max_turns=200, run_config=run_config)
    return result