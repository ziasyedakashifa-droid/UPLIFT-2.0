import json
import urllib.request
import urllib.error


# Friend's laptop running Ollama
OLLAMA_URL = "http://192.168.50.140:11434/api/chat"
MODEL = "gemma4:e2b"


def analyse_journal(text):

    prompt = f"""
You are a non-clinical student wellbeing reflection assistant.

Analyse the student's journal reflection and return ONLY valid JSON.

Use exactly these keys:
- emotions: array of emotions
- stressors: array of stressors
- support_message: two empathetic sentences
- suggestion: one low-risk practical step
- support_option: one helpful option

Rules:
- Do not diagnose any medical or mental health condition.
- Do not predict self-harm or assess safety.
- Do not prescribe treatment or medication.
- Do not claim certainty.
- Use only details explicitly present in the reflection.
- Be gentle, supportive and concise.
- Do not include Markdown or explanations outside JSON.

Student reflection:
{text}
"""

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False,
        "format": "json",
        "think": False
    }

    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            result = json.loads(response.read().decode("utf-8"))

        raw = result.get("message", {}).get("content", "").strip()

        if not raw:
            raise ValueError("Gemma returned an empty response.")

        analysis = json.loads(raw)

        required_keys = [
            "emotions",
            "stressors",
            "support_message",
            "suggestion",
            "support_option"
        ]

        for key in required_keys:
            if key not in analysis:
                raise ValueError(f"Gemma response is missing: {key}")

        return analysis

    except urllib.error.URLError as error:
        raise RuntimeError(
            f"Could not connect to Ollama. Check whether your friend's "
            f"laptop and Ollama server are running. Details: {error}"
        )

    except json.JSONDecodeError:
        raise ValueError("Gemma did not return valid JSON.")
