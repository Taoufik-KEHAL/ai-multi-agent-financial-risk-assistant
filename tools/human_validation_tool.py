def ask_human_validation(final_answer: str) -> dict:
    """
    Demande une validation humaine avant décision finale.
    """

    print("\n================ VALIDATION HUMAINE ================\n")
    print(final_answer)
    print("\n====================================================\n")

    decision = input("Valider cette décision ? (oui/non) : ").strip().lower()

    if decision == "oui":
        return {
            "validated": True,
            "message": "Décision validée par l'utilisateur."
        }

    return {
        "validated": False,
        "message": "Décision refusée par l'utilisateur."
    }