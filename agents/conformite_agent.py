from graph.state import AgentState

from tools.conformite_retriever import search_conformite
from tools.procedure_retriever import search_procedures

from langchain_ollama import ChatOllama


# Initialisation du modèle
model = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)


def conformite_agent(state: AgentState) -> AgentState:
    """
    Agent conformité :
    utilise le RAG documentaire
    pour analyser le dossier client.
    """

    question = state["question"]

    # Recherche documentaire
    conformite_context = search_conformite(question)

    procedure_context = search_procedures(question)

    # Prompt
    prompt = f"""
    Tu es un expert conformité et recouvrement.

    Analyse la situation du client
    à partir des documents suivants.

    === RÈGLES DE CONFORMITÉ ===
    {conformite_context}

    === PROCÉDURES DE RECOUVREMENT ===
    {procedure_context}

    Question utilisateur :
    {question}

    Fournis :
    - une analyse conformité
    - les risques détectés
    - les procédures applicables
    - une recommandation finale
    """

    # Appel LLM
    response = model.invoke(prompt)

    analysis = response.content

    print("[CONFORMITE AGENT] Analyse conformité générée")

    state["conformite_analysis"] = analysis

    return state