from pathlib import Path


PROMPTS_DIR = Path("prompts")


def load_prompt(name: str) -> str:
    prompt_path = PROMPTS_DIR / name

    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt introuvable : {prompt_path}")

    return prompt_path.read_text(encoding="utf-8").strip()
