from pathlib import Path
from datetime import datetime
import json
from rich.console import Console
from rich.markdown import Markdown

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

    #if filename is None:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename}_{timestamp}"

    file_path = output_path / f"{filename}.md"

    with file_path.open("w", encoding=encoding) as f:
        f.write(markdown_text.strip() + "\n")

    return file_path

def save_json(result, output_dir="outputs", filename=None):
    # save markdown as json
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"crawl_{timestamp}"
    file_path = output_path / f"{filename}.json"

    with file_path.open("w", encoding="utf-8") as f:
        json.dump(result.final_output.model_dump(), f, indent=2, ensure_ascii=False)

    return file_path

def print_markdown(result):
    console = Console()
    console.print(Markdown(result.final_output))

def json_to_markdown(data: dict) -> str:
    lines = []
    for page in data["pages"]:
        # Page header
        lines.append(f"# {page['title']}")
        lines.append(f"*URL: {page['url']}*")
        lines.append("")
        # Intro instruction
        if page.get("instruction"):
            lines.append(page["instruction"])
            lines.append("")
        # Sections
        for section in page.get("sections", []):
            lines.append(f"## {section['heading']}")
            lines.append("")
            for block in section.get("blocks", []):
                if block.get("title"):
                    lines.append(f"### {block['title']}")
                    lines.append("")
                for segment in block.get("segments", []):
                    lines.append(segment["text"])
                    lines.append("")
        # Contact
        if page.get("contact"):
            lines.append("## Kontakt")
            lines.append("")
            lines.append(page["contact"])
            lines.append("")
        # Page separator
        lines.append("---")
        lines.append("")

    return "\n".join(lines)

def save_markdown_from_json(json_path: str, md_path: str) -> None:
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    
    markdown = json_to_markdown(data)
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown)

if __name__ == "__main__":
    save_markdown_from_json(
        json_path="outputs/Netze-Strom.json",
        md_path="outputs/Netze-Strom.md"
    )