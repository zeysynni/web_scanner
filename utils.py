from pathlib import Path
from datetime import datetime
import json
from rich.console import Console
from rich.markdown import Markdown
import pypandoc
import os

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

    for page in data.get("pages", []):
        # Page metadata
        lines.append(f"*URL: {page.get('url', '')}*")
        lines.append("")

        # Blocks
        for block in page.get("blocks", []):
            lines.append(f"## {block.get('heading', '')}")
            lines.append("")

            # Segments
            for segment in block.get("segments", []):
                if segment.get("subheading"):
                    lines.append(f"### {segment['subheading']}")
                    lines.append("")
                if segment.get("text"):
                    lines.append(segment["text"])
                    lines.append("")
                if segment.get("files"):
                    lines.append("**Dateien:**")
                    lines.append(segment["files"])
                    lines.append("")
                if segment.get("FAQs"):
                    faq = segment["FAQs"]
                    if faq.get("title"):
                        lines.append(f"### {faq['title']}")
                        lines.append("")
                    for qa in faq.get("QAs", []):
                        lines.append(f"**{qa.get('question', '')}**")
                        lines.append("")
                        lines.append(qa.get("answer", ""))
                        lines.append("")
                if segment.get("contacts"):
                    lines.append("**Kontakt:**")
                    lines.append(segment["contacts"])
                    lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)
    
def save_markdown_from_json(json_path: str, md_path: str) -> None:
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    
    markdown = json_to_markdown(data)
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown)

def md_to_pdf(input_md_path: str, output_pdf_path: str):
    """
    Convert a Markdown (.md) file to a PDF file.

    Args:
        input_md_path (str): Path to the input .md file
        output_pdf_path (str): Path to save the output .pdf file
    """
    if not os.path.exists(input_md_path):
        raise FileNotFoundError(f"Input file not found: {input_md_path}")

    try:
        pypandoc.convert_file(
            input_md_path,
            to="pdf",
            outputfile=output_pdf_path,
            extra_args=["--pdf-engine=xelatex"]  # or pdflatex
        )
        print(f"PDF successfully created at: {output_pdf_path}")
    except Exception as e:
        raise RuntimeError(f"Conversion failed: {e}")

if __name__ == "__main__":
    # save json to md
    input_path = Path("rest/Unternehmen_0.json")
    output_path = input_path.with_suffix(".md")

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    markdown = json_to_markdown(data)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"Saved to {output_path}")