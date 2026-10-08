from .models import DocumentChunk, PageText


def _join_until_limit(parts: list[str], size: int) -> list[str]:
    chunks: list[str] = []
    current = ""
    for part in parts:
        candidate = f"{current}\n\n{part}".strip() if current else part
        if len(candidate) <= size:
            current = candidate
            continue
        if current:
            chunks.append(current)
        current = part
    if current:
        chunks.append(current)
    return chunks


def chunk_text(text: str, chunk_size: int = 6000, chunk_overlap: int = 500) -> list[DocumentChunk]:
    if not text.strip():
        return []

    paragraphs = [part.strip() for part in text.split("\n\n") if part.strip()]
    rough_chunks = _join_until_limit(paragraphs, chunk_size)

    chunks: list[DocumentChunk] = []
    previous_tail = ""
    for index, chunk in enumerate(rough_chunks, start=1):
        chunk_text_value = f"{previous_tail}\n\n{chunk}".strip() if previous_tail else chunk
        chunks.append(DocumentChunk(chunk_id=index, text=chunk_text_value))
        previous_tail = chunk[-chunk_overlap:] if chunk_overlap > 0 else ""
    return chunks


def chunk_pages(
    pages: list[PageText],
    chunk_size: int = 6000,
    chunk_overlap: int = 500,
) -> list[DocumentChunk]:
    if not pages:
        return []

    chunks: list[DocumentChunk] = []
    current_text = ""
    start_page: int | None = None
    end_page: int | None = None
    previous_tail = ""

    for page in pages:
        page_text = page.text.strip()
        if not page_text:
            continue

        candidate = f"{current_text}\n\n{page_text}".strip() if current_text else page_text
        if len(candidate) <= chunk_size:
            current_text = candidate
            start_page = start_page or page.page
            end_page = page.page
            continue

        if current_text:
            chunks.append(
                DocumentChunk(
                    chunk_id=len(chunks) + 1,
                    text=f"{previous_tail}\n\n{current_text}".strip() if previous_tail else current_text,
                    start_page=start_page,
                    end_page=end_page,
                )
            )
            previous_tail = current_text[-chunk_overlap:] if chunk_overlap > 0 else ""

        current_text = page_text
        start_page = page.page
        end_page = page.page

    if current_text:
        chunks.append(
            DocumentChunk(
                chunk_id=len(chunks) + 1,
                text=f"{previous_tail}\n\n{current_text}".strip() if previous_tail else current_text,
                start_page=start_page,
                end_page=end_page,
            )
        )

    return chunks
