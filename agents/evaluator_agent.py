from graph.state import AgentState

from langchain_ollama import ChatOllama


# Initialisation du modèle
model = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)


def evaluator_agent(state: AgentState) -> AgentState:
    """
    Agent évaluateur :
    combine les analyses financières et conformité
    puis génère une décision finale.
    """

    financial_analysis = state["financial_analysis"]

    conformite_analysis = state["conformite_analysis"]

    prompt = f"""
    Tu es un expert en analyse du risque client.

    Tu dois analyser les éléments suivants
    et produire une décision finale.

    === ANALYSE FINANCIÈRE ===
    {financial_analysis}

    === ANALYSE CONFORMITÉ ===
    {conformite_analysis}

    Fournis :
    1. Une synthèse globale
    2. Le niveau de risque :
       - faible
       - moyen
       - élevé
    3. Les risques détectés
    4. Une recommandation finale
    5. Indiquer si une validation humaine est nécessaire
    """

    response = model.invoke(prompt)

    final_answer = response.content

    print("[EVALUATOR AGENT] Décision finale générée")

    state["final_answer"] = final_answer

    return state