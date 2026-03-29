from pydantic import BaseModel, Field
from typing import List, Optional

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
        "Either a question-answer pair, or some general information listed as heading-details pair. "
        "Look for the clickable plus button, if you find it, then it might belongs to here"
        "This could have the name 'FAQ' or 'Allgemeine Informationen' or similar. "
        "Exact text copied from the webpage. "
    )

class ContentSegment(BaseModel):
    text: Optional[str] = Field(
        default=None,
        description=(
            "A paragraph of textual description or list of subtopics."
            "Exact text copied from the webpage. "
            "If it contains contact information or tables, keep it in the paragraph. "
            "Do not summarize, shorten, or paraphrase."
            "Doesn't belong to text: FAQ or Fragen. "
            "Make sure to use Markdown"
        )
    )
    table: Optional[str] = Field(
        default=None,
        description=(
            "A table of information. "
            "Exact text copied from the webpage in markdown. "
            "Do not summarize, shorten, or paraphrase."
            "If the table has a topic, make sure to write it down. "
        )
    )
    files: Optional[str] = Field(
        default=None,
        description=(
            "Names of all files listed in this area, mostly for downloading. "
            "Files are mostly PDFs"
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
            "Questions (with ? at the end of the sentence) or text (Hinweis or Information) with clickalbe drop down, where you have to click on the plus button to show more."
            "If you see clickable plus buttons, it DEFINITELY belongs to this part! "
            "Make sure to click the clickable plus button and then wait for 0.5 seconds to have the answer shown. "
            "Typical FAQs object could relate to Allgemeine Information, FAQ, Fragen, Hinweis etc. "
        )
    )

class Block(BaseModel):
    heading: str = Field(
        description=(
        "Visible heading exactly as shown on the webpage. "
        "Mostly the size of words are the biggest or with color. "
        "Do not invent headings."
        "Make sure to use Markdown"
    )
    )
    subheading: Optional[str] = Field(
        description=(
        "Visible subheading. "
        "Follows mostly directly after the heading, could also appear after a block. "
        "Mostly the size of words are bigger than normal texts and smaller than heading. "
        "Do not invent headings."
        "Make sure to use Markdown"
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
        description="URL of the crawled webpage, make sure this is the true URL of the webpage. Everytime you click into a new webpage, write down the URL. "
    )
    block: List[Block] = Field(
        description="A block of content with a heading/subheading from the webpage. Make sure use markdown for everything. Also make sure to separate different blocks according to context. Mostly, a page contains several blocks. ",
        example="Wir sind für Sie da ..."
    )

class Webpages(BaseModel):
    base_url: str
    pages: list[Page] = Field(
        description="Everytime you click on a subtopic and enters a new webpage, it is a new Page object. "
    )