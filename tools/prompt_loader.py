from pathlib import Path


DOSSIER_PROMPTS = Path("prompts")


def charger_prompt(nom: str) -> str:
    chemin_prompt = DOSSIER_PROMPTS / nom

    if not chemin_prompt.exists():
        raise FileNotFoundError(f"Prompt introuvable : {chemin_prompt}")

    return chemin_prompt.read_text(encoding="utf-8").strip()
