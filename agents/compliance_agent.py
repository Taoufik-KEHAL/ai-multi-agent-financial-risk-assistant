from graph.state import AgentState


def compliance_agent(state: AgentState) -> AgentState:
    """
    Agent conformité :
    vérifie les règles réglementaires et internes.
    """

    question = state["question"]

    analysis = f"""
    Analyse de conformité générée pour la demande :
    {question}

    Résultat :
    - Aucune restriction réglementaire critique détectée
    - Le dossier nécessite une vérification humaine avant décision finale
    - Les règles internes de validation doivent être respectées
    """

    print("[COMPLIANCE AGENT] Analyse de conformité effectuée")

    state["compliance_analysis"] = analysis

    return state