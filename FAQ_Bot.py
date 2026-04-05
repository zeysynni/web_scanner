import asyncio
from contextlib import AsyncExitStack
from dotenv import load_dotenv
from knowledge_graph_db_agent import launch_DB, create_faq_agent
from agents import trace
import gradio as gr

load_dotenv(override=True)

async def ask(question: str, history: list):
    async with AsyncExitStack() as stack:
        agent = await create_faq_agent(stack)
        with trace("FAQ"):
            result = await launch_DB(agent, topic="qa", message=question)
        return result.final_output

demo = gr.ChatInterface(
    fn=ask,
    title="Stadtwerke Waiblingen FAQ Bot",
    description="Stellen Sie Ihre Fragen zu Strom, Gas und Wärme.",
    type="messages",
)

if __name__ == "__main__":
    demo.launch()