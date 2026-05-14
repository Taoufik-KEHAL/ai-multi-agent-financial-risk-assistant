from graph.state import EtatAgent


def agent_superviseur(etat: EtatAgent) -> EtatAgent:
    question = etat["question"].lower()

    if "finance" in question or "financier" in question or "financière" in question:
        route = "finance"

    elif "conformité" in question or "réglementation" in question or "reglementation" in question:
        route = "conformite"

    else:
        route = "both"

    print(f"[SUPERVISOR] Route choisie : {route}")

    etat["route"] = route
    return etat
