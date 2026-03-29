from pydantic import BaseModel, Field
from typing import List, Optional, Union, Literal

# A general structure for parsing webpages of Stadtwerke Waiblingen
    
class ContentBlock(BaseModel):
    type: str = Field(
        description=(
            "Type of content block on the webpage. "
            "Examples: paragraph, list, faq, table, contact, text"
        )
    )

    title: Optional[str] = Field(
        description=(
            "Title of the block if visible on the webpage "
            "(e.g. FAQ question or accordion title)."
        )
    )

    content: str = Field(
        description=(
        "Full text extracted exactly from the webpage. "
        "Do not summarize or paraphrase or omit."
        "Preserve line breaks and lists."
        )
    )

class Section(BaseModel):

    heading: str = Field(
        description="Heading of this section exactly as shown on the webpage."
    )

    blocks: List[ContentBlock] = Field(
        description=(
            "All content blocks belonging to this section in the same order "
            "as they appear on the webpage."
        )
    )

class Webpage(BaseModel):

    url: str = Field(
        description="URL of the crawled webpage."
    )

    title: str = Field(
        description="Main page title (usually H1)."
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


