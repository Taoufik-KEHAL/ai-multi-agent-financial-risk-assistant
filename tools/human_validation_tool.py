VALIDATION_ACCEPTED = {"oui", "o", "yes", "y", "valider", "validé", "valide"}
VALIDATION_REFUSED = {"non", "n", "no", "refuser", "refusé", "refuse"}


def ask_human_validation(
    final_answer: str,
    decision: str | None = None,
    comment: str = "",
    allow_console: bool = True,
) -> dict:
    """
    Demande ou applique une validation humaine avant décision finale.
    """

    if decision is None and allow_console:
        print("\n================ VALIDATION HUMAINE ================\n")
        print(final_answer)
        print("\n====================================================\n")

        decision = input("Valider cette décision ? (oui/non) : ")

    if decision is None:
        return {
            "status": "pending",
            "validated": False,
            "message": "Décision en attente de validation humaine.",
            "comment": comment,
        }

    normalized_decision = decision.strip().lower()

    if normalized_decision in VALIDATION_ACCEPTED:
        return {
            "status": "validated",
            "validated": True,
            "message": "Décision validée par l'utilisateur.",
            "comment": comment,
        }

    if normalized_decision in VALIDATION_REFUSED:
        return {
            "status": "refused",
            "validated": False,
            "message": "Décision refusée par l'utilisateur.",
            "comment": comment,
        }

    return {
        "status": "pending",
        "validated": False,
        "message": f"Décision humaine non reconnue : {decision}",
        "comment": comment,
    }
