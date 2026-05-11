from langgraph.graph import StateGraph, END

from graph.state import AgentState

from agents.supervisor import supervisor_agent
from agents.financial_agent import financial_agent
from agents.conformite_agent import conformite_agent
from agents.evaluator_agent import evaluator_agent
from agents.human_validation_agent import human_validation_agent


# Création du graphe
workflow = StateGraph(AgentState)


# Ajout des nodes
workflow.add_node("supervisor", supervisor_agent)
workflow.add_node("financial", financial_agent)
workflow.add_node("conformite", conformite_agent)
workflow.add_node("evaluator", evaluator_agent)
workflow.add_node("human_validation", human_validation_agent)


# Point d'entrée
workflow.set_entry_point("supervisor")


# Edges du workflow
workflow.add_edge("supervisor", "financial")
workflow.add_edge("financial", "conformite")
workflow.add_edge("conformite", "evaluator")
workflow.add_edge("evaluator", "human_validation")
workflow.add_edge("human_validation", END)


# Compilation du graph
app = workflow.compile()