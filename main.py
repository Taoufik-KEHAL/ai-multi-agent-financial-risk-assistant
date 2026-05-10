from graph.workflow import app


initial_state = {
    "question": "Analyse financière du client C015",
    "route": "",
    "financial_analysis": "",
    "conformite_analysis": "",
    "risk_level": "",
    "final_answer": "",
    "documents": []
}


result = app.invoke(initial_state)

print("\n================ RESULTAT FINAL ================\n")

print(result["financial_analysis"])

print("\n================================================\n")