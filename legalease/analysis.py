import json
from typing import Any

from .chunker import chunk_pages, chunk_text
from .llm_client import LLMClient, demo_chunk_analysis
from .models import DocumentChunk, ProcessedDocument
from .prompt_manager import PromptManager
from .response_parser import ensure_final_report, parse_json_response


def build_chunks(processed: ProcessedDocument, config: dict[str, Any]) -> list[DocumentChunk]:
    chunk_config = config.get("chunking", {})
    chunk_size = int(chunk_config.get("chunk_size", 6000))
    chunk_overlap = int(chunk_config.get("chunk_overlap", 500))

    if processed.pages:
        return chunk_pages(processed.pages, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return chunk_text(processed.cleaned_text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)


def analyze_document(
    processed: ProcessedDocument,
    user_type: str,
    document_type: str,
    specific_concern: str,
    config: dict[str, Any],
) -> dict[str, Any]:
    prompts = PromptManager()
    client = LLMClient(config)
    chunks = build_chunks(processed, config)
    max_chunks = int(config.get("analysis", {}).get("max_chunks", 8))
    chunks = chunks[:max_chunks]

    chunk_analyses: list[dict[str, Any]] = []
    for chunk in chunks:
        if client.has_api_key:
            prompt = prompts.render(
                "chunk_analysis_prompt.txt",
                user_type=user_type,
                document_type=document_type,
                specific_concern=specific_concern or "No specific concern provided.",
                page_range=chunk.page_range,
                chunk_text=chunk.text,
            )
            raw = client.complete(prompt)
            chunk_analyses.append(parse_json_response(raw))
        else:
            chunk_analyses.append(demo_chunk_analysis(chunk.page_range))

    if client.has_api_key:
        final_prompt = prompts.render(
            "final_synthesis_prompt.txt",
            user_type=user_type,
            document_type=document_type,
            specific_concern=specific_concern or "No specific concern provided.",
            chunk_analyses=json.dumps(chunk_analyses, indent=2),
        )
        raw_final = client.complete(final_prompt)
        return ensure_final_report(parse_json_response(raw_final))

    return ensure_final_report(
        {
            "short_summary": "Demo mode: configure LLM_API_KEY to generate a full AI explanation.",
            "what_this_means_for_me": (
                f"As a {user_type.lower()}, you should review the highlighted obligations, rights, "
                "deadlines, fees, and risk areas before relying on this document."
            ),
            "important_obligations": _collect(chunk_analyses, "obligations"),
            "user_rights": _collect(chunk_analyses, "rights"),
            "deadlines": _collect(chunk_analyses, "deadlines"),
            "fees_and_penalties": _collect(chunk_analyses, "fees_or_penalties"),
            "potential_risks": _collect(chunk_analyses, "potential_risks"),
            "important_clauses": _collect(chunk_analyses, "important_clauses"),
            "questions_to_consider": _collect(chunk_analyses, "questions_to_consider"),
            "source_references": _collect(chunk_analyses, "source_references"),
        }
    )


def _collect(items: list[dict[str, Any]], key: str) -> list[str]:
    values: list[str] = []
    for item in items:
        raw_values = item.get(key, [])
        if isinstance(raw_values, str):
            raw_values = [raw_values]
        for value in raw_values:
            if value and value not in values:
                values.append(str(value))
    return values
