import re

from graph.state import EtatAgent
from config.llm import obtenir_llm
from tools.client_data_tool import recuperer_donnees_client
from tools.prompt_loader import charger_prompt


modele = obtenir_llm()
PROMPT_FINANCIER = charger_prompt("financial.txt")


def agent_financier(etat: EtatAgent) -> EtatAgent:
    """
    Agent financier :
    analyse les données financières du client
    depuis le fichier CSV.
    """

    question = etat["question"]

    correspondance_client = re.search(r"\bC\d{3}\b", question.upper())
    identifiant_client = (
        correspondance_client.group(0) if correspondance_client else None
    )

    if not identifiant_client:
        etat["analyse_financiere"] = "Identifiant client introuvable."
        return etat

    # Appel du tool CSV
    resultat = recuperer_donnees_client(identifiant_client)

    if not resultat["trouve"]:
        etat["analyse_financiere"] = resultat["message"]
        return etat

    client = resultat["donnees_client"]

    prompt = PROMPT_FINANCIER.format(
        question=question,
        client_id=client["client_id"],
        prenom=client["prenom"],
        nom=client["nom"],
        age=client["age"],
        situation=client["situation"],
        nombre_enfants=client["nombre_enfants"],
        activite=client["activite"],
        revenu_mensuel_mad=client["revenu_mensuel_mad"],
        encours_mad=client["encours_mad"],
        retard_jours=client["retard_jours"],
        incidents_paiement=client["incidents_paiement"],
        echeance_janvier=client["echeance_janvier"],
        echeance_fevrier=client["echeance_fevrier"],
        echeance_mars=client["echeance_mars"],
        niveau_risque=client["niveau_risque"],
    )

    reponse = modele.invoke(prompt)
    analyse = reponse.content

    print(f"[FINANCIAL AGENT] Analyse du client {identifiant_client} effectuée")

    etat["analyse_financiere"] = analyse

    return etat
