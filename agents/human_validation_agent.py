from graph.state import AgentState
from tools.human_validation_tool import ask_human_validation


def human_validation_agent(state: AgentState) -> AgentState:
    """
    Agent de validation humaine :
    demande à l'utilisateur de valider ou refuser
    la décision finale proposée par le système.
    """

    final_answer = state["final_answer"]

    validation_result = ask_human_validation(final_answer)

    state["is_validated"] = validation_result["validated"]
    state["human_validation"] = validation_result["message"]

    if validation_result["validated"]:
        state["final_answer"] += "\n\nDécision finale : VALIDÉE par l'utilisateur."
    else:
        state["final_answer"] += "\n\nDécision finale : REFUSÉE par l'utilisateur."

    print("[HUMAN VALIDATION] Validation humaine effectuée")

    return state