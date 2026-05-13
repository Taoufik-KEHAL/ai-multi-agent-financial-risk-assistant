import re

from graph.state import AgentState
from config.llm import get_llm
from tools.client_data_tool import get_client_data
from tools.prompt_loader import load_prompt


model = get_llm()
FINANCIAL_PROMPT = load_prompt("financial.txt")


def financial_agent(state: AgentState) -> AgentState:
    """
    Agent financier :
    analyse les données financières du client
    depuis le fichier CSV.
    """

    question = state["question"]

    client_match = re.search(r"\bC\d{3}\b", question.upper())
    client_id = client_match.group(0) if client_match else None

    if not client_id:
        state["financial_analysis"] = "Identifiant client introuvable."
        return state

    # Appel du tool CSV
    result = get_client_data(client_id)

    if not result["found"]:
        state["financial_analysis"] = result["message"]
        return state

    client = result["client_data"]

    prompt = FINANCIAL_PROMPT.format(
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

    response = model.invoke(prompt)
    analysis = response.content

    print(f"[FINANCIAL AGENT] Analyse du client {client_id} effectuée")

    state["financial_analysis"] = analysis

    return state
