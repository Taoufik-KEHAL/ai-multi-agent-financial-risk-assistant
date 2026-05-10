from graph.state import AgentState


def financial_agent(state: AgentState) -> AgentState:
    """
    Agent financier :
    analyse le risque financier du client.
    """

    question = state["question"]

    analysis = f"""
    Analyse financière générée pour la demande :
    {question}

    Résultat :
    - Historique de paiement acceptable
    - Quelques retards mineurs
    - Niveau de solvabilité moyen
    """

    print("[FINANCIAL AGENT] Analyse financière effectuée")

    state["financial_analysis"] = analysis

    return state