from graph.state import AgentState


def supervisor_agent(state: AgentState) -> AgentState:
    question = state["question"].lower()

    if "finance" in question or "financier" in question or "financière" in question:
        route = "finance"

    elif "conformité" in question or "réglementation" in question or "reglementation" in question:
        route = "compliance"

    else:
        route = "both"

    print(f"[SUPERVISOR] Route choisie : {route}")

    state["route"] = route
    return state