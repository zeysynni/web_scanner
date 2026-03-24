from pydantic import BaseModel, Field
from typing import List, Optional, Union, Literal

# The structure for Netze/Strom
class QA(BaseModel):
    question: str = Field(
        description=(
            "A question or a heading-like text in this block. "
            "Exact text copied from the webpage. "
            )
    )
    answer:str = Field(
        description=(
            "The answer to this question or details to the heading-like text, make sure to click on the plus button and wait for 0.5 seconds to get this shown. "
            "Exact text copied from the webpage. "
            )
    )

class FAQ(BaseModel):
    QAs: List[QA] = Field (
        description=
        "A question-answer pair, or heading-details pair. "
        "Exact text copied from the webpage. "
    )

class ContentSegment(BaseModel):
    text: Optional[str] = Field(
        default=None,
        description=(
            "A textual description of a certain topic."
            "Exact text copied from the webpage. "
            "Do not summarize, shorten, or paraphrase."
        )
    )
    table: Optional[str] = Field(
        default=None,
        description=(
            "A table of information. "
            "Exact text copied from the webpage in markdown. "
            "Do not summarize, shorten, or paraphrase."
        )
    )
    files: Optional[str] = Field(
        default=None,
        description=(
            "Names of all files listed in this area. "
            "Exact text copied from the webpage. "
            "Do not summarize, shorten, or paraphrase."
        )
    )
    contacts: Optional[str] = Field(
        default=None,
        description=(
            "Contact information. "
            "Exact text copied from the webpage. "
            "Do not summarize, shorten, or paraphrase."
        ),
        json_schema_extra={"example": "Telefon"}
    )
    FAQs: Optional[FAQ] = Field(
        default=None,
        description=(
            "All the question-answer pairs shown in this block. Make sure to click the clickable plus button and then wait for 0.5 seconds to have the answer shown. "
        )
    )

class Block(BaseModel):
    heading: str = Field(
        description=(
        "Visible heading exactly as shown on the webpage. "
        "Do not invent headings."
    )
    )
    segments: List[ContentSegment] = Field(
        description=(
            "A segment represents the content of a Block, it consists of ContentSegments, which represent a type of content."
            "It could be texts which explains the heading, an FAQ element, a table that is crawled down in markdown, names of several files, contact information."
        )
    )

class Page(BaseModel):
    url: str = Field(
        description="URL of the crawled webpage."
    )

    title: str = Field(
        description="Main page title (usually H1)."
    )
    intro: Optional[str] = Field(
        description=(
            "The introduction to the main title. "
        )
    )
    block: List[Block] = Field(
        description="a block of content with a heading from the webpage. ",
        example="Wir sind für Sie da ..."
    )

class Webpages(BaseModel):
    base_url: str
    pages: list[Page]
