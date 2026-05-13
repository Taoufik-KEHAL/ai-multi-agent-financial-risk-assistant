from graph.state import AgentState

from tools.conformite_retriever import search_conformite
from tools.procedure_retriever import search_procedures
from tools.prompt_loader import load_prompt

from config.llm import get_llm


# Initialisation du modèle
model = get_llm()
CONFORMITE_PROMPT = load_prompt("conformite.txt")


def conformite_agent(state: AgentState) -> AgentState:
    """
    Agent conformité :
    utilise le RAG documentaire
    pour analyser le dossier client.
    """

    question = state["question"]
    financial_analysis = state["financial_analysis"]

    # Recherche documentaire
    rag_query = f"{question}\n\n{financial_analysis}"

    conformite_context = search_conformite(rag_query)

    procedure_context = search_procedures(rag_query)

    prompt = CONFORMITE_PROMPT.format(
        question=question,
        financial_analysis=financial_analysis,
        conformite_context=conformite_context,
        procedure_context=procedure_context,
    )

    # Appel LLM
    response = model.invoke(prompt)

    analysis = response.content

    print("[CONFORMITE AGENT] Analyse conformité générée")

    state["conformite_analysis"] = analysis

    return state
