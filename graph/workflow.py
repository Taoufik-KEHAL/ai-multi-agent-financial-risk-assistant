import warnings

from langchain_core._api.deprecation import LangChainPendingDeprecationWarning

warnings.filterwarnings(
    "ignore",
    message=".*allowed_objects.*",
    category=LangChainPendingDeprecationWarning,
)

from langgraph.graph import StateGraph, END

from graph.state import EtatAgent

from agents.supervisor import agent_superviseur
from agents.financial_agent import agent_financier
from agents.conformite_agent import agent_conformite
from agents.evaluator_agent import agent_evaluateur
from agents.human_validation_agent import agent_validation_humaine


# Création du graphe
flux_travail = StateGraph(EtatAgent)


# Ajout des nodes
flux_travail.add_node("superviseur", agent_superviseur)
flux_travail.add_node("financier", agent_financier)
flux_travail.add_node("conformite", agent_conformite)
flux_travail.add_node("evaluateur", agent_evaluateur)
flux_travail.add_node("validation_humaine", agent_validation_humaine)


# Point d'entrée
flux_travail.set_entry_point("superviseur")


# Edges du workflow
flux_travail.add_edge("superviseur", "financier")
flux_travail.add_edge("financier", "conformite")
flux_travail.add_edge("conformite", "evaluateur")
flux_travail.add_edge("evaluateur", "validation_humaine")
flux_travail.add_edge("validation_humaine", END)


# Compilation du graph
application = flux_travail.compile()
