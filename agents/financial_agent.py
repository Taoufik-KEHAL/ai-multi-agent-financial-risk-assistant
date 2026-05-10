from graph.state import AgentState
from tools.client_data_tool import get_client_data


def financial_agent(state: AgentState) -> AgentState:
    """
    Agent financier :
    analyse les données financières du client
    depuis le fichier CSV.
    """

    question = state["question"]

    # Extraction simple de l'identifiant client
    words = question.split()

    client_id = None

    for word in words:
        if word.startswith("C"):
            client_id = word.upper()

    if not client_id:
        state["financial_analysis"] = "Identifiant client introuvable."
        return state

    # Appel du tool CSV
    result = get_client_data(client_id)

    if not result["found"]:
        state["financial_analysis"] = result["message"]
        return state

    client = result["client_data"]

    analysis = f"""
    Analyse financière du client {client['client_id']} :

    Informations personnelles :
    - Nom : {client['prenom']} {client['nom']}
    - Activité : {client['activite']}
    - Situation familiale : {client['situation']}
    - Nombre d'enfants : {client['nombre_enfants']}

    Situation financière :
    - Revenu mensuel : {client['revenu_mensuel_mad']} MAD
    - Encours : {client['encours_mad']} MAD
    - Retard : {client['retard_jours']} jours
    - Incidents de paiement : {client['incidents_paiement']}

    Échéances :
    - Janvier : {client['echeance_janvier']}
    - Février : {client['echeance_fevrier']}
    - Mars : {client['echeance_mars']}

    Niveau de risque estimé :
    - {client['niveau_risque']}
    """

    print(f"[FINANCIAL AGENT] Analyse du client {client_id} effectuée")

    state["financial_analysis"] = analysis

    return state