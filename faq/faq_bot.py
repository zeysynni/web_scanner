from contextlib import AsyncExitStack
from dotenv import load_dotenv
from faq.knowledge_graph_db_agent import launch_DB, create_faq_agent
from mcp_params import sqlite_db_params, knowledge_graph_db_params
from prompts import qa_instruction_sql, qa_instruction_kg
from agents import trace
import gradio as gr

load_dotenv(override=True)

# switch db between knowledge-graph and sql
db_params = sqlite_db_params
qa_instruction = qa_instruction_sql

async def ask(question: str, history: list) -> str:
    async with AsyncExitStack() as stack:
        agent = await create_faq_agent(stack, qa_instruction, db_params)
        messages = []
        for turn in history:
            messages.append({"role": "user", "content": turn["content"] if isinstance(turn, dict) else turn[0]})
            messages.append({"role": "assistant", "content": turn["content"] if isinstance(turn, dict) else turn[1]})
        
        # Append current question
        messages.append({"role": "user", "content": question})

        #with trace("FAQ"):
        result = await launch_DB(agent, topic="qa", message=messages)

        return result.final_output

demo = gr.ChatInterface(
    fn=ask,
    title="Stadtwerke Waiblingen FAQ Bot",
    description="Stellen Sie Ihre Fragen zu Strom, Gas und Wärme.",
    type="messages",
)

if __name__ == "__main__":
    demo.launch()