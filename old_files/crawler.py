from agents import Agent, Tool, Runner, trace, Tool, RunConfig
from contextlib import AsyncExitStack
from agents.mcp import MCPServerStdio
from agents.models.openai_provider import OpenAIProvider
import openai
from rich.markdown import Markdown
from rich.console import Console
import asyncio
from dotenv import load_dotenv
import os
from IPython.display import display, Markdown

# for asyncio in jupyter notebook
import nest_asyncio
nest_asyncio.apply()

load_dotenv(override=True)

playwright_params = {"command": "npx","args": [ "@playwright/mcp@latest"], "client_timeout": 30}
web_scraping_mcp_params = [playwright_params]

web_crawling_instructions = """
Du bist der Web-Scraping-Agent. Deine Aufgabe ist es, Webseiten sorgfältig zu lesen und gezielt FAQ-Inhalte und die FAQ-relevanten-Inhalte (wie z.B. 'Sie haben Fragen?') vollständig zu extrahieren.

Allgemeine Anweisungen:
- Prüfe beim Öffnen einer Webseite immer auf Cookie-Consent-Banner.
- Falls ein Button wie "Alle akzeptieren", "Akzeptieren" oder "Accept all" sichtbar ist, klicke diesen zuerst, bevor du irgendetwas anderes tust.
- Interagiere mit Navigationselementen erst, nachdem alle Overlays geschlossen wurden.

Inhaltserfassung – NUR FAQ-Bereiche und die FAQ-relevanten-Inhalte (wie z.B. 'Sie haben Fragen?'):
- Navigiere zu jedem angegebenen Thema und Unterthema.
- Ignoriere alle anderen Inhalte (Einleitungstexte, Werbung, allgemeinef Beschreibungen).
- Fokussiere dich ausschließlich auf FAQ-Abschnitte und FAQ-relevante-Abschnitte innerhalb jedes Themas.
- Erfasse JEDES Frage-Antwort-Paar vollständig und wörtlich – genau so, wie es auf der Webseite steht.
- Kürze, paraphrasiere oder verändere keine Fragen oder Antworten.

Anweisung für angehängte Dokumente (PDF / Formulare):
- Falls an eine Frage oder Antwort ein PDF oder Formular angehängt ist, schreibe NICHT den Inhalt heraus.
- Vermerke stattdessen: "📎 [Typ: PDF/Formular] – [Kurzbeschreibung worum es geht] – Zu finden unter: [Abschnitt/Link/Position auf der Seite]"

Ausgabeformat:
- Erstelle eine vollständige Dokumentation im Markdown-Format.
- Strukturiere die Dokumentation entsprechend der vorgegebenen Themen und Unterthemen.
- Jedes Frage-Antwort-Paar wird exakt so wiedergegeben:
  **F: [Frage]**
  A: [Antwort]
- Kein FAQ-Paar darf fehlen.
"""

message = f"""
Bitte analysiere die folgende Webseite: {url}

Navigiere zu den folgenden Themen und Unterthemen und extrahiere ausschließlich die FAQ-Inhalte und die FAQ-relevanten-Inhalte (wie z.B. 'Sie haben Fragen?') aus jedem Bereich:

- Strom
  - Ökostrom
  - Wärmestrom
  - Grundversorgung
  - Preisinformation
  - Stromkennzeichnung
- Erdgas
  - Grundversorgung
- Wasser
- Wärme
  - Fernwärme
  - Mobile Heizzentralen mieten
- E-Mobilität
  - Anmeldung E-Ladestation
- Bäder
- Service
  - Zählerstand mitteilen
  - Umzugsservice
  - Abrechnung & Zahlung
  - Abschläge berechnen & verstehen
  - Energiesparen
  - Warnung vor Betrugsversuchen

Vorgehensweise:
1. Öffne die Webseite und schließe alle Cookie-Banner.
2. Navigiere nacheinander zu jedem oben genannten Thema und Unterthema.
3. Suche in jedem Bereich gezielt nach dem FAQ-Abschnitt und dem FAQ-relevanten-Abschnitt.
4. Erfasse jedes Frage-Antwort-Paar vollständig und wörtlich – genau so wie auf der Seite.
5. Falls ein PDF oder Formular angehängt ist, notiere: Typ, worum es geht, und wo es zu finden ist – aber schreibe den Inhalt NICHT heraus.
6. Ignoriere alle anderen Inhalte außerhalb der FAQ-Bereiche und FAQ-relevanten-Bereiche.

Ausgabe:
Erstelle eine strukturierte Markdown-Dokumentation mit folgender Gliederung:

# [Thema]
## [Unterthema]
### FAQ
**F: [Frage]**
A: [Antwort]

📎 [Typ: PDF/Formular] – [Kurzbeschreibung] – Zu finden unter: [Position/Link]
"""

url = "https://www.stadtwerke-waiblingen.de/Privatkunden/Strom"

from pathlib import Path
from datetime import datetime

#@function_tool
def save_markdown(markdown_text: str,output_dir: str = "outputs",filename: str | None = None,encoding: str = "utf-8") -> Path:
    """
    Speichert Markdown-Text lokal in einer .md-Datei.

    Args:
        markdown_text: Der Markdown-Inhalt (String)
        output_dir: Zielordner (wird erstellt, falls nicht vorhanden)
        filename: Dateiname ohne Endung; falls None → Zeitstempel
        encoding: Text-Encoding (Standard: utf-8)

    Returns:
        Path zur gespeicherten Datei
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"documentation_{timestamp}"

    file_path = output_path / f"{filename}.md"

    with file_path.open("w", encoding=encoding) as f:
        f.write(markdown_text.strip() + "\n")

    return file_path

    # Create a client with built-in retry logic
openai_client = openai.AsyncOpenAI(
    max_retries=5,  # retry up to 5 times
)

run_config = RunConfig(
    model_provider=OpenAIProvider(openai_client=openai_client)
)

async def create_mcp_servers(stack: AsyncExitStack):
    craw_servers = [await stack.enter_async_context(MCPServerStdio({**params,"timeout": 120})) for params in playwright_params]
    return craw_servers

async def create_craw_agent(stack: AsyncExitStack) -> Agent:
    craw_server = await create_mcp_servers(stack)
    agent = Agent(
        name="agent", 
        instructions=web_crawling_instructions, 
        model="gpt-4.1-mini", 
        mcp_servers=[craw_server]
    )
    return agent
    
async def chat_with_agent(manager: Agent, message = message):
    with trace("Crawler Test"):
        result = await Runner.run(manager, message, max_turns=100, REQUEST_TIMEOUT=120)
    return result

async def main():
    async with AsyncExitStack() as stack:
        crawler = await create_craw_agent(stack)
        result = await chat_with_agent(crawler)
    display(Markdown(result.final_output))
    save_markdown(
        markdown_text=result.final_output, 
        output_dir="/Users/sunzeyuan/projects/agent_exercises/agents/crawler", 
        filename="Zusammenfassung"
        )
