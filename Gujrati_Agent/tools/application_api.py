import random

def submit_application(scheme_id: str, profile: dict, documents: list) -> dict:
    # Simulate a small failure rate for resilience testing
    if random.random() < 0.05:
        return {"ok": False, "error": "સર્વર સમયસર પ્રતિસાદ આપતો નથી"}
    app_id = f"APP-{scheme_id}-{random.randint(10000,99999)}"
    return {
        "ok": True,
        "application_id": app_id,
        "status": "સ્વીકાર્યું",
        "next_steps": "પોર્ટલ પર દસ્તાવેજો અપલોડ કરો અને SMS/ઈમેઇલ દ્વારા અપડેટ્સ મેળવો."
    }
