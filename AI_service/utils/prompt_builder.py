def build_diagnosis_prompt(symptoms: list[str], vehicle_info: str) -> str:
    symptom_text = ", ".join(symptoms) if symptoms else "no symptoms provided"
    return (
        "You are an automotive diagnostic assistant. "
        f"Vehicle info: {vehicle_info}. "
        f"Symptoms: {symptom_text}. "
        "Provide likely causes and next steps."
    )
