from graph.state import AgentState
from tools.human_validation_tool import ask_human_validation


def human_validation_agent(state: AgentState) -> AgentState:
    """
    Agent de validation humaine :
    demande à l'utilisateur de valider ou refuser
    la décision finale proposée par le système.
    """

    final_answer = state.get("decision_draft", state["final_answer"])
    decision = state.get("human_decision")
    comment = state.get("human_comment", "")
    allow_console = state.get("allow_console_validation", True)

    validation_result = ask_human_validation(
        final_answer=final_answer,
        decision=decision,
        comment=comment,
        allow_console=allow_console,
    )

    state["decision_draft"] = final_answer
    state["is_validated"] = validation_result["validated"]
    state["human_validation"] = validation_result["message"]
    status = validation_result["status"]

    if status == "validated":
        state["final_answer"] += "\n\nDécision finale : VALIDÉE par l'utilisateur."
    elif status == "refused":
        state["final_answer"] += "\n\nDécision finale : REFUSÉE par l'utilisateur."
    else:
        state["final_answer"] += "\n\nDécision finale : EN ATTENTE de validation humaine."

    if validation_result["comment"]:
        state["final_answer"] += f"\nCommentaire humain : {validation_result['comment']}"

    print("[HUMAN VALIDATION] Validation humaine effectuée")

    return state
