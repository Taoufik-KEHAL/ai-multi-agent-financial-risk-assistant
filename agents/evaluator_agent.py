from graph.state import EtatAgent

from config.llm import obtenir_llm
from tools.prompt_loader import charger_prompt


# Initialisation du modèle
modele = obtenir_llm()
PROMPT_EVALUATEUR = charger_prompt("evaluator.txt")


def agent_evaluateur(etat: EtatAgent) -> EtatAgent:
    """
    Agent évaluateur :
    combine les analyses financières et conformité
    puis génère une décision finale.
    """

    analyse_financiere = etat["analyse_financiere"]

    analyse_conformite = etat["analyse_conformite"]

    prompt = PROMPT_EVALUATEUR.format(
        analyse_financiere=analyse_financiere,
        analyse_conformite=analyse_conformite,
    )

    reponse = modele.invoke(prompt)

    reponse_finale = reponse.content
    reponse_finale_minuscule = reponse_finale.lower()

    if "niveau de risque retenu : élevé" in reponse_finale_minuscule:
        etat["niveau_risque"] = "élevé"
    elif "niveau de risque retenu : moyen" in reponse_finale_minuscule:
        etat["niveau_risque"] = "moyen"
    elif "niveau de risque retenu : faible" in reponse_finale_minuscule:
        etat["niveau_risque"] = "faible"

    print("[EVALUATOR AGENT] Décision finale générée")

    etat["brouillon_decision"] = reponse_finale
    etat["reponse_finale"] = reponse_finale

    return etat
