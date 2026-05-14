from graph.state import EtatAgent

from tools.conformite_retriever import rechercher_conformite
from tools.procedure_retriever import rechercher_procedures
from tools.prompt_loader import charger_prompt

from config.llm import obtenir_llm


# Initialisation du modèle
modele = obtenir_llm()
PROMPT_CONFORMITE = charger_prompt("conformite.txt")


def agent_conformite(etat: EtatAgent) -> EtatAgent:
    """
    Agent conformité :
    utilise le RAG documentaire
    pour analyser le dossier client.
    """

    question = etat["question"]
    analyse_financiere = etat["analyse_financiere"]

    # Recherche documentaire
    requete_rag = f"{question}\n\n{analyse_financiere}"

    contexte_conformite = rechercher_conformite(requete_rag)

    contexte_procedure = rechercher_procedures(requete_rag)

    prompt = PROMPT_CONFORMITE.format(
        question=question,
        analyse_financiere=analyse_financiere,
        contexte_conformite=contexte_conformite,
        contexte_procedure=contexte_procedure,
    )

    # Appel LLM
    reponse = modele.invoke(prompt)

    analyse = reponse.content

    print("[CONFORMITE AGENT] Analyse conformité générée")

    etat["analyse_conformite"] = analyse

    return etat
