VALIDATION_ACCEPTEE = {"oui", "o", "yes", "y", "valider", "validé", "valide"}
VALIDATION_REFUSEE = {"non", "n", "no", "refuser", "refusé", "refuse"}


def demander_validation_humaine(
    reponse_finale: str,
    decision: str | None = None,
    commentaire: str = "",
    autoriser_console: bool = True,
) -> dict:
    """
    Demande ou applique une validation humaine avant décision finale.
    """

    if decision is None and autoriser_console:
        print("\n================ VALIDATION HUMAINE ================\n")
        print(reponse_finale)
        print("\n====================================================\n")

        decision = input("Valider cette décision ? (oui/non) : ")

    if decision is None:
        return {
            "statut": "en_attente",
            "valide": False,
            "message": "Décision en attente de validation humaine.",
            "commentaire": commentaire,
        }

    decision_normalisee = decision.strip().lower()

    if decision_normalisee in VALIDATION_ACCEPTEE:
        return {
            "statut": "valide",
            "valide": True,
            "message": "Décision validée par l'utilisateur.",
            "commentaire": commentaire,
        }

    if decision_normalisee in VALIDATION_REFUSEE:
        return {
            "statut": "refuse",
            "valide": False,
            "message": "Décision refusée par l'utilisateur.",
            "commentaire": commentaire,
        }

    return {
        "statut": "en_attente",
        "valide": False,
        "message": f"Décision humaine non reconnue : {decision}",
        "commentaire": commentaire,
    }
