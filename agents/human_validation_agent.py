from graph.state import EtatAgent
from tools.human_validation_tool import demander_validation_humaine


def nettoyer_decision_finale(reponse: str) -> str:
    lignes = []

    for ligne in reponse.splitlines():
        ligne_normalisee = ligne.strip().lower()

        if ligne_normalisee.startswith("décision finale :"):
            continue
        if ligne_normalisee.startswith("commentaire humain :"):
            continue
        if ligne_normalisee.startswith("commentaires :"):
            continue

        lignes.append(ligne)

    return "\n".join(lignes).strip()


def agent_validation_humaine(etat: EtatAgent) -> EtatAgent:
    """
    Agent de validation humaine :
    demande à l'utilisateur de valider ou refuser
    la décision finale proposée par le système.
    """

    reponse_finale = nettoyer_decision_finale(
        etat.get("brouillon_decision", etat["reponse_finale"])
    )
    decision = etat.get("decision_humaine")
    commentaire = etat.get("commentaire_humain", "")
    autoriser_console = etat.get("autoriser_validation_console", True)

    resultat_validation = demander_validation_humaine(
        reponse_finale=reponse_finale,
        decision=decision,
        commentaire=commentaire,
        autoriser_console=autoriser_console,
    )

    etat["brouillon_decision"] = reponse_finale
    etat["est_valide"] = resultat_validation["valide"]
    etat["validation_humaine"] = resultat_validation["message"]
    statut = resultat_validation["statut"]

    if statut == "valide":
        resume_decision = "Décision finale : le dossier a été validé."
    elif statut == "refuse":
        resume_decision = "Décision finale : le dossier a été refusé."
    else:
        resume_decision = "Décision finale : EN ATTENTE de validation humaine."

    etat["reponse_finale"] = f"{reponse_finale}\n\n{resume_decision}"

    if resultat_validation["commentaire"]:
        etat["reponse_finale"] += (
            f"\nCommentaires : {resultat_validation['commentaire']}"
        )

    print("[HUMAN VALIDATION] Validation humaine effectuée")

    return etat
