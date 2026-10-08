from dataclasses import dataclass, field


@dataclass
class PageText:
    page: int | None
    text: str


@dataclass
class DocumentStats:
    word_count: int
    sentence_count: int
    character_count: int
    paragraph_count: int
    average_sentence_length: float


@dataclass
class ProcessedDocument:
    original_text: str
    cleaned_text: str
    sentences: list[str]
    tokens: list[str]
    stats: DocumentStats
    pages: list[PageText] = field(default_factory=list)


@dataclass
class DocumentChunk:
    chunk_id: int
    text: str
    start_page: int | None = None
    end_page: int | None = None

    @property
    def page_range(self) -> str:
        if self.start_page is None and self.end_page is None:
            return "Not available"
        if self.start_page == self.end_page:
            return f"Page {self.start_page}"
        return f"Pages {self.start_page}-{self.end_page}"
