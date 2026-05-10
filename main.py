from graph.workflow import app


initial_state = {
    "question": "Analyse financière du client C102",
    "route": "",
    "financial_analysis": "",
    "compliance_analysis": "",
    "risk_level": "",
    "final_answer": "",
    "documents": []
}


result = app.invoke(initial_state)

print(result["final_answer"])