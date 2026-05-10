from langgraph.graph import StateGraph, END

from graph.state import AgentState

from agents.supervisor import supervisor_agent
from agents.financial_agent import financial_agent
from agents.compliance_agent import compliance_agent
from agents.evaluator_agent import evaluator_agent


# Création du graphe
workflow = StateGraph(AgentState)


# Ajout des nodes
workflow.add_node("supervisor", supervisor_agent)
workflow.add_node("financial", financial_agent)
workflow.add_node("compliance", compliance_agent)
workflow.add_node("evaluator", evaluator_agent)


# Point d'entrée
workflow.set_entry_point("supervisor")


# Edges du workflow
workflow.add_edge("supervisor", "financial")
workflow.add_edge("financial", "compliance")
workflow.add_edge("compliance", "evaluator")
workflow.add_edge("evaluator", END)


# Compilation du graph
app = workflow.compile()