from pathlib import Path
from typing import Any


class PromptManager:
    def __init__(self, prompt_dir: str | Path = "prompts") -> None:
        self.prompt_dir = Path(prompt_dir)

    def load(self, name: str) -> str:
        path = self.prompt_dir / name
        return path.read_text(encoding="utf-8")

    def render(self, name: str, **values: Any) -> str:
        template = self.load(name)
        rendered = template
        for key, value in values.items():
            rendered = rendered.replace("{" + key + "}", str(value))
        return rendered
