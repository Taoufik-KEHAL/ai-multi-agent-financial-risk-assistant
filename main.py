from graph.workflow import app


initial_state = {
    "question": "Le client C015 peut-il obtenir une validation malgré plusieurs retards de paiement ?",
    "route": "",
    "financial_analysis": "",
    "conformite_analysis": "",
    "risk_level": "",
    "final_answer": "",
    "documents": []
}


result = app.invoke(initial_state)

print("\n================ RESULTAT FINAL ================\n")

print(result["final_answer"])

print("\n================================================\n")