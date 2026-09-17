# Veridian Corp — Internal Service Agent (Assignment 2)

A policy-grounded internal IT service agent built for the AIONOS Agentic AI Factory assignment.

## What it demonstrates
- Understand employee issue / intent
- Retrieve the most relevant supplied policy using TF-IDF semantic similarity
- Use ticket history as precedent/context
- Resolve simple requests
- Ask follow-up questions for unclear requests
- Escalate risky or authority-sensitive requests
- Create a structured ticket for routed/escalated cases
- Show the exact source policy used
- Maintain an in-memory audit trail

## Source discipline
The agent uses only the supplied assignment data pack:
- `data/policies.json`
- `data/requests.json`
- `data/tickets.json`

No external company policies are invented.

## Run locally
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app:app --reload
```

Open `http://127.0.0.1:8000`.

## Fast one-command run
After installing requirements:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

## Suggested demo scenarios
1. VPN expired → grounded resolution + TK-1042 precedent.
2. Phishing email → immediate Security escalation + warning not to forward.
3. Guest Wi-Fi → direct resolution, no ticket.
4. Laptop dead → hardware escalation and policy conflict/early-replacement context.
5. “hey can you help, its not working” → follow-up question rather than guessing.
6. Contractor VPN → manager approval route.
7. Expense tool → Finance route because IT does not grant access.

## API endpoints
- `GET /` — web prototype
- `POST /ask` — agent query
- `POST /request/{REQ-ID}` — test supplied request
- `GET /audit` — audit trail
- `GET /tickets` — ticket history

## Important implementation note
The agent is intentionally deterministic and source-grounded for this assessment. The retrieval component is AI/NLP-based (TF-IDF + cosine similarity), while decision policies are explicit so the reviewer can audit why the agent acted. This avoids hallucinating company policy.
