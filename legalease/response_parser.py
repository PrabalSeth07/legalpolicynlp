import json
import re
from typing import Any


JSON_BLOCK_PATTERN = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL)


def parse_json_response(raw_text: str) -> dict[str, Any]:
    text = raw_text.strip()
    match = JSON_BLOCK_PATTERN.search(text)
    if match:
        text = match.group(1)

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return {"raw_response": raw_text}

    return parsed if isinstance(parsed, dict) else {"items": parsed}


def ensure_final_report(data: dict[str, Any]) -> dict[str, Any]:
    defaults: dict[str, Any] = {
        "short_summary": "",
        "what_this_means_for_me": "",
        "important_obligations": [],
        "user_rights": [],
        "deadlines": [],
        "fees_and_penalties": [],
        "potential_risks": [],
        "important_clauses": [],
        "questions_to_consider": [],
        "source_references": [],
        "disclaimer": "This is an informational explanation, not legal advice.",
    }
    return {**defaults, **data}
