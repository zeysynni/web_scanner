# LLM-Powered Web Crawler

## Overview

This project implements an **LLM-powered web crawler** that extracts structured content from websites and converts it into Markdown and PDF formats.

Instead of traditional scraping, the system uses an agent-based approach with structured outputs to intelligently navigate and parse web pages.

---

## Key Features

* 🔍 Agent-based web crawling using LLMs
* 🧠 Structured extraction with Pydantic schemas
* 📄 Automatic conversion: JSON → Markdown → PDF
* ⚙️ Modular and extensible architecture
* 🔁 Async pipeline for scalable crawling

---

## Architecture

The system is organized into modular components:

```
.
├── main.py                 # Entry point
├── crawl_agent.py          # Agent + crawling logic
├── webpage_structure.py    # Pydantic data schema
├── utils.py                # Formatting and file handling
├── prompts.py              # LLM instructions
├── config.py               # Crawl configuration
├── mcp_params.py           # MCP server configuration
├── outputs/                # Generated results
├── faq/                    # FAQ Bot relevant files, provide two variants of databases (knowledge-graph-based and sql)
├── faq/db_agent.py         # DB Agent
├── faq/ingest_kg.py        # ingest .md files from crawl results to knowledge-graph-based DB. Run this to do new ingestion
├── faq/ingest_sql.py       # ingest .md files from crawl results to sql DB. Run this to do new ingestion
├── faq/faq_bot.py          # Launch for running the FAQ Bot
```

### Pipeline

1. Define crawl targets in `config.py`
2. Generate structured prompts
3. Agent crawls and extracts structured data
4. Save results as JSON
5. Convert JSON → Markdown → PDF

---

## Data Model

The crawler outputs structured data using Pydantic models:

* `Webpages`
* `Page`
* `Block`
* `ContentSegment`
* `Case-dependent structures like FAQ / QA`

This ensures:

* consistent structure
* easy post-processing
* compatibility with downstream pipelines

---

## Installation

```bash
git clone https://github.com/your-username/llm-web-crawler.git
cd llm-web-crawler
pip install -r requirements.txt
```

---

## Environment Setup

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

---

## Usage

Run the crawler:

```bash
python main.py
```

Outputs will be saved in (for .pdf files you will have to run md2pdf.py explicitly):

```
outputs/
├── topic.json
├── topic.md
├── topic.pdf
```
You will find the predefined relevant cralwing goals from a webpage/webpages in the file config.py. There you can switch from different webpages that need to be crawled.

You might wants to adjust webpage structure under the file webpage_structure.py, do this only if needed.

---

## Example Output

### JSON (structured)

```json
{
  "pages": [
    {
      "url": "...",
      "blocks": [...]
    }
  ]
}
```

### Markdown (generated)

```
## Section Title

### Subheading
Content...

**Files**
- example.pdf
```

---

## Design Principles

This project follows:

* **Separation of concerns** (agent, schema, utils)
* **Single Responsibility Principle**
* **Explicit data modeling with Pydantic**
* **Decoupling of data and processing logic**
* **Async-first architecture**

---

## Limitations

* Depends on LLM accuracy
* Requires careful prompt design for best results

---

## Future Improvements

* Introduce rate limiting
* Add CLI interface
* Add unit tests

---

## Extras

* In the folder **faq**, an FAQ-Bot with two variants of DB, based on the crawl results, is implemented. 
* Information are extracted from .md files of the crawl results.
* A Gradio UI is provided.
* Chat history is implemented as list of messages.

---

## License

MIT License
