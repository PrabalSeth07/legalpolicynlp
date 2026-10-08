from pathlib import Path
from typing import BinaryIO

from pypdf import PdfReader

from .models import PageText


def extract_pdf_pages(file_obj: BinaryIO) -> list[PageText]:
    reader = PdfReader(file_obj)
    pages: list[PageText] = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append(PageText(page=index, text=text.strip()))
    return pages


def extract_txt(file_obj: BinaryIO) -> str:
    raw = file_obj.read()
    if isinstance(raw, bytes):
        return raw.decode("utf-8", errors="replace")
    return str(raw)


def pages_to_text(pages: list[PageText]) -> str:
    return "\n\n".join(page.text for page in pages if page.text)


def load_sample_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")
