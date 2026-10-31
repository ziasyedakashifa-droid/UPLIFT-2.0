# UPLIFT 2.0 Starter

Flask prototype: Gemma-powered journal reflection, mood check-ins, demo human-support requests and a demo counsellor view.

## Windows setup
1. Extract ZIP and open this folder in VS Code.
2. Open Terminal > New Terminal.
3. Run:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```
If activation is blocked:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```
4. Copy `.env.example` to `.env`. Add your API key and the exact Gemma 4 model ID supported by your provider.
5. Run `python app.py` and open http://127.0.0.1:5000.

## Gemma configuration
`gemma.py` uses Google's `google-genai` SDK. The selected provider must expose the exact Gemma 4 model through this SDK. Model IDs and availability vary; verify them with your provider rather than guessing.

## Demo
- MoodMap: save a mood check-in.
- MindMirror: enter a fictional, non-sensitive reflection and request an AI reflection.
- HumanConnect: submit a demo support request.
- Demo counsellor: view the locally stored demo request.

## Critical limitations
This is NOT a medical service, diagnostic tool or crisis-response system. The phrase-based safety check is incomplete, can miss urgent situations and is not a risk assessment. Do not use real student mental-health data. The counsellor page has no authentication and the SQLite database stores journal text in plain form. The support form does not contact a real counsellor. Do not deploy publicly or use with real students without clinical review, security review, proper authentication/authorisation, encryption, consent, deletion/retention controls and a staffed escalation process. Use fictional demo data only.
