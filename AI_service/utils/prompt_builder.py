def build_diagnosis_prompt(symptoms: list[str], vehicle_info: str) -> str:
    symptom_text = ", ".join(symptoms) if symptoms else "no symptoms provided"
    return (
        "You are an automotive diagnostic assistant. "
        f"Vehicle info: {vehicle_info}. "
        f"Symptoms: {symptom_text}. "
        "Provide likely causes and next steps."
        "With the following format:\n"
        "Likely causes:\n"
        "- Cause 1\n"
        "- Cause 2\n"
        "Next steps:\n"
        "- Step 1\n"
        "- Step 2\n"
        "double check the information and provide a concise, clear response."
        "Only exact matches to the symptoms should be considered. Make sure to match the car brand or model if provided. If no likely causes can be determined, respond with 'No likely causes found.'"
    )
