import re

from .models import DocumentStats, PageText, ProcessedDocument


SENTENCE_PATTERN = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")
TOKEN_PATTERN = re.compile(r"\b[\w'-]+\b")


def normalize_whitespace(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_sentences(text: str) -> list[str]:
    if not text.strip():
        return []
    parts = SENTENCE_PATTERN.split(text)
    return [sentence.strip() for sentence in parts if sentence.strip()]


def tokenize(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(text)


def calculate_stats(text: str, sentences: list[str], tokens: list[str]) -> DocumentStats:
    paragraphs = [part for part in text.split("\n\n") if part.strip()]
    sentence_count = len(sentences)
    average = round(len(tokens) / sentence_count, 2) if sentence_count else 0.0
    return DocumentStats(
        word_count=len(tokens),
        sentence_count=sentence_count,
        character_count=len(text),
        paragraph_count=len(paragraphs),
        average_sentence_length=average,
    )


def preprocess_document(text: str, pages: list[PageText] | None = None) -> ProcessedDocument:
    cleaned = normalize_whitespace(text)
    sentences = split_sentences(cleaned)
    tokens = tokenize(cleaned)
    stats = calculate_stats(cleaned, sentences, tokens)
    return ProcessedDocument(
        original_text=text,
        cleaned_text=cleaned,
        sentences=sentences,
        tokens=tokens,
        stats=stats,
        pages=pages or [],
    )
