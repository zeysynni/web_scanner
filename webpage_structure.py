from pydantic import BaseModel, Field
from typing import List, Optional, Union, Literal

# The structure for Netze/Strom
class ContentSegment(BaseModel):
    text: str = Field(
        description=(
            "Exact text copied from the webpage. "
            "Do not summarize, shorten, or paraphrase."
            "Could also be a hint of a file."
        )
    )

class Block(BaseModel):
    title: Optional[str] = Field(
        description=(
            "Title of the block if visible on the webpage "
            "(e.g. FAQ question or accordion title)."
            "Do not invent titles."
        )
    )
    segments: List[ContentSegment] = Field(
        description=(
            "Each segment should represent a logical subpart such as "
            "a paragraph, list item, or subsection."
        )
    )

class Section(BaseModel):
    heading: str = Field(
        description=(
        "Visible heading exactly as shown on the webpage. "
        "Do not invent headings. If no heading exists, use the nearest visible title."
    )
    )
    blocks: List[Block] = Field(
        description=(
            "All content blocks belonging to this section in the same order "
            "as they appear on the webpage."
        )
    )

class Page(BaseModel):
    url: str = Field(
        description="URL of the crawled webpage."
    )

    title: str = Field(
        description="Main page title (usually H1)."
    )
    instruction: Optional[str] = Field(
        description="instructional text before all the sections. ",
        example="Wir sind für Sie da ..."
    )
    sections: List[Section] = Field(
        description="All sections appearing on the webpage."
    )
    contact: Optional[str] = Field(
        description=(
            "Contact information if present on the page. "
            "Copy exactly from the webpage."
        )
    )

class Webpages(BaseModel):
    base_url: str
    pages: list[Page]
