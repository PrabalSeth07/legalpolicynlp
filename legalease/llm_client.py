import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAIError, RateLimitError


class LLMClient:
    def __init__(self, config: dict[str, Any]) -> None:
        load_dotenv()
        self.config = config
        self.api_key = os.getenv("LLM_API_KEY", "")
        self.base_url = os.getenv("LLM_BASE_URL") or None

    @property
    def has_api_key(self) -> bool:
        return bool(self.api_key.strip())

    def complete(self, prompt: str) -> str:
        if not self.has_api_key:
            raise RuntimeError("LLM_API_KEY is not configured.")

        from openai import OpenAI

        llm_config = self.config.get("llm", {})
        client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        try:
            response = client.chat.completions.create(
                model=llm_config.get("model", "gpt-4o-mini"),
                temperature=llm_config.get("temperature", 0.2),
                max_tokens=llm_config.get("max_tokens", 3000),
                messages=[
                    {
                        "role": "system",
                        "content": "You are LegalEase. Explain documents clearly without giving legal advice.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
        except RateLimitError as exc:
            raise RuntimeError(
                "OpenAI API quota is exhausted. Add credits in OpenAI billing or remove the API key to use demo mode."
            ) from exc
        except OpenAIError as exc:
            raise RuntimeError(f"OpenAI API request failed: {exc}") from exc

        return response.choices[0].message.content or ""


def demo_chunk_analysis(page_range: str) -> dict[str, Any]:
    return {
        "summary": f"This section contains legal or policy terms from {page_range}.",
        "obligations": ["Review any duties, restrictions, or required actions mentioned in this section."],
        "rights": ["Check whether this section gives the user any explicit rights or protections."],
        "deadlines": [],
        "fees_or_penalties": [],
        "important_clauses": ["Important clauses may require careful reading before accepting the document."],
        "potential_risks": ["Some terms may affect the user's responsibilities or options."],
        "questions_to_consider": ["Is there anything in this section you do not understand or cannot comply with?"],
        "source_references": [page_range],
    }
