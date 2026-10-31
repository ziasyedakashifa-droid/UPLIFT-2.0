# Crude demo phrase check only. NOT clinical risk detection and may miss urgent situations.
PHRASES=["kill myself","suicide","end my life","hurt myself","self-harm","self harm","don't want to live","do not want to live"]
def urgent_support_message(text):
    if any(p in text.lower() for p in PHRASES):
        return ("Your message may describe an immediate safety concern. This app cannot provide crisis care. "
                "Please contact local emergency services or a trusted person now and seek qualified human support. "
                "If you are in immediate danger, go to the nearest emergency department. Do not wait for an AI response.")
    return None
