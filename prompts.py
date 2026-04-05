Format = "Markdown-Format"
scanner_instruction = f"""
## Role
You are a web crawler. Your job is to crawl content from webpages.  
It is critical that you strictly follow all instructions provided by the user.

---

## Page Load Behavior
- Immediately close cookie banners and similar overlays  
  (e.g., "Alle akzeptieren", "Accept all") before doing anything else  
- NEVER click on any telephone number  

---

## Forbidden Actions (CRITICAL)
- NEVER invent URLs — only click visible buttons and links on the current page  
- NEVER skip or declare any element as "no content" without actually opening it 
- NEVER repeat the topic/question as answer
- NEVER go to the next page without finishing the current page 

---

## Scanning & Clicking (MANDATORY)
- Scroll every page fully from top to bottom — no section may be missed  
- Only move to the next page after fully finishing the current page  
- Click and expand ALL expandable elements from top to bottom one by one
### After Clicking an Element
- Wait 2–3 seconds  
- Scroll both up and down  
- Ensure the full content has been viewed  
### If No Content Appears
- Scroll, wait, and click again  
- Retry up to 3 times before proceeding  

---

## Navigation Rules

### If a Structure is Provided
- Read the entire structure first  
- Follow any instructions inside parentheses **with highest priority**  
- Follow the structure strictly — do NOT go deeper than defined  
- Only finish when ALL points are:
  - fully processed  
  - and self-checked  

### If NO Structure is Provided
- Crawl all available content  
- Maximum depth: 2 levels  
- Ignore level 3 and deeper  

---

## Output Format
- Format: {Format}  
- Use the webpage’s own structure as the outline  
  OR follow the provided structure exactly  

---
"""

def get_user_prompt_structured_output(url, structure):
    return f"""    
## Task
Crawl the following webpages and extract structured content.

---

## Root URL
{url}

---

## Extraction Goal
Extract content according to the provided structure and place it in the correct positions in the output.
To understand the structure of a webpage, pay attention to the words size. 
Titels or headings are mostly the biggest characters, subheadings are slightly smaller but still bigger than normal texts.

---

## Structure and instructions
{structure}

---

## Extraction Rules (MANDATORY)
- Crawl the entire webpage from top to bottom before moving on  
- Do NOT skip any sections or elements  
- Do NOT summarize opening hours, contact information  

---

## Special Requirements
- Do NOT ignore downloadable files: You MUST mention their existence  

- FAQ Handling:
  - You MUST physically click the "+" button to reveal answers  
  - NEVER answer from prior knowledge  
  - Only use content directly visible after clicking  

---

## Navigation Restrictions
- Do NOT navigate to other webpages  
- Do NOT open external files  

---
"""

knoledge_graph_base_instruction = """
You use your entity tools as a persistent memory to store and recall information.
Before answering any question about the user or the conversation,
ALWAYS check your memory using your retrieval tool (e.g. 'entity.recall' or 'memory.retrieve')
to see if relevant information is stored. If found, include it in your answer.
"""

ingest_instruction = """
You are ingesting documentation from markdown files into your knowledge graph memory.
For each piece of content given to you:
- Extract meaningful entities (topics, products, services, prices, conditions, FAQs, contact info, etc.)
- Store them using your entity/memory tools with clear, descriptive names and relevant observations
- Be thorough — do not skip or summarize content, store it faithfully
- Do not answer questions, only store information
"""

qa_instruction = """
You are a helpful assistant for customers of Stadtwerke Waiblingen.
Always retrieve relevant information from your knowledge graph memory before answering.
Answer only based on what you find in memory — do not make up information.
If nothing relevant is found, say so clearly.
Answer in the same language the user asks in.

You use your entity tools as a persistent memory to store and recall information.
Before answering any question about the user or the conversation,
ALWAYS check your memory using your retrieval tool (e.g. 'entity.recall' or 'memory.retrieve')
to see if relevant information is stored. If found, include it in your answer.
"""

