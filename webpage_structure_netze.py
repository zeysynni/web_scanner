from pydantic import BaseModel, Field
from typing import List, Optional, Union, Literal

# The structure for Netze/Strom
class QA(BaseModel):
    question: str = Field(
        description=(
            "A question or a heading-like text in this block. "
            "Make sure to click on the clickable plus button and wait for 0.5 seconds to get content shown! "
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
        "Mostly a question-answer pair, or some general information listed as heading-details pair. "
        "Look for the clickable plus button, if you find it, then it might belongs to here"
        "This could have the name 'FAQ' or 'Allgemeine Informationen' or similar. "
        "Exact text copied from the webpage. "
    )

class ContentSegment(BaseModel):
    text: Optional[str] = Field(
        default=None,
        description=(
            "A textual description of a certain topic."
            "Exact text copied from the webpage. "
            "If it contains contact information or tables, keep it in the paragraph. "
            "Do not summarize, shorten, or paraphrase."
            "If you have to click a button to see the content, then it definitly doesn't belong to this, it belongs to the FAQ section. "
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
            "Names of all files listed in this area, mostly for downloading. "
            "Files are mostly PDFs"
            "Exact text copied from the webpage. "
            "Do not summarize, shorten, or paraphrase."
        ),
        json_schema_extra={"example": "...PDF"}
    )
    contacts: Optional[str] = Field(
        default=None,
        description=(
            "Contact information. "
            "Telefon numbers are important, but E-Mail should be ignored. "
            "Also write down what is the telefon number for. "
            "Exact text copied from the webpage. "
            "Do not summarize, shorten, or paraphrase."
        )
    )
    FAQs: Optional[FAQ] = Field(
        default=None,
        description=(
            "Question-Answer pairs or clickalbe drop down text with both titel and content, where you have to click on the plus button to get information shown."
            "If you see clickable plus buttons, it DEFINITELY belongs to this part! "
            "Make sure to click the clickable plus button and then wait for 0.5 seconds to have the answer shown. "
            "Typical FAQs could be 'Allgemeine Information', 'FAQ' etc. "
        )
    )

class Block(BaseModel):
    heading: str = Field(
        description=(
        "Visible heading exactly as shown on the webpage. "
        "Mostly the size of words are bigger or with color. "
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
        description="URL of the crawled webpage, make sure this is the true URL of the webpage."
    )
    block: List[Block] = Field(
        description="A block of content with a heading from the webpage.",
        example="Wir sind für Sie da ..."
    )

class Webpages(BaseModel):
    base_url: str
    pages: list[Page]

