from contextlib import AsyncExitStack
import asyncio
from dotenv import load_dotenv

from prompts import scanner_instruction, get_user_prompt_structured_output
from crawl_agent import create_craw_agent, launch_crawler
from config import *
from utils import *

load_dotenv(override=True)
# note separate strucutre more, also items to crawl. uplodad to github

instructions = scanner_instruction

async def main():
    async with AsyncExitStack() as stack:
        agent = await create_craw_agent(stack)
        for topic, config in structure.items():
            url = config.get("url")
            k = 0
            for subpart in config.get("subpart", []):
                message = get_user_prompt_structured_output(url, subpart)
                subtopic = topic + "_" + str(k)
                await launch_crawler(agent, subtopic, message)
                save_markdown_from_json(json_path=f"outputs/{subtopic}.json", md_path=f"outputs/{subtopic}.md")
                k += 1
            k = 0

if __name__ == "__main__":
    asyncio.run(main())