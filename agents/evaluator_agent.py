from graph.state import AgentState


def evaluator_agent(state: AgentState) -> AgentState:
    """
    Agent évaluateur :
    combine les analyses finance et conformité
    puis détermine le niveau de risque.
    """

    financial_analysis = state["financial_analysis"]
    compliance_analysis = state["compliance_analysis"]

    if "retards mineurs" in financial_analysis.lower():
        risk_level = "moyen"
    else:
        risk_level = "faible"

    final_answer = f"""
    Synthèse finale du dossier :

    Analyse financière :
    {financial_analysis}

    Analyse conformité :
    {compliance_analysis}

    Niveau de risque estimé : {risk_level.upper()}

    Recommandation :
    Le dossier peut être poursuivi, mais il nécessite une validation humaine avant toute décision finale.
    """

    print(f"[EVALUATOR AGENT] Niveau de risque estimé : {risk_level}")

    state["risk_level"] = risk_level
    state["final_answer"] = final_answer

    return state