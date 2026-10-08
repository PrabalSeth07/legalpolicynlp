from legalease.chunker import chunk_pages, chunk_text
from legalease.models import PageText


def test_chunk_text_returns_chunks():
    chunks = chunk_text("Para one.\n\nPara two.", chunk_size=20, chunk_overlap=0)
    assert len(chunks) == 2
    assert chunks[0].chunk_id == 1


def test_chunk_pages_preserves_page_range():
    pages = [PageText(page=1, text="A" * 10), PageText(page=2, text="B" * 10)]
    chunks = chunk_pages(pages, chunk_size=15, chunk_overlap=0)
    assert chunks[0].start_page == 1
    assert chunks[1].start_page == 2
