# EduSwarm AI — Personalized Learning with a Team of AI Agents

EduSwarm AI is an educational support prototype for students who have limited access to one-to-one tutoring. It uses the **Strands Agents SDK** to coordinate specialist agents that explain concepts, create practice questions, and identify learning gaps.

## What is included
- FastAPI backend
- Strands Agents SDK multi-agent architecture (orchestrator + Tutor, Quiz, and Learning Coach agents)
- Responsive Arabic/English web interface
- Safe local demo mode for trying the UI without AWS credentials
- AWS Bedrock integration through Strands when demo mode is disabled

## Architecture
1. **Orchestrator Agent** receives the learner's request and delegates to specialists.
2. **Tutor Agent** explains a concept step-by-step, adapting the explanation to the learner's level.
3. **Quiz Agent** creates practice questions and gives feedback.
4. **Learning Coach Agent** diagnoses likely knowledge gaps and proposes a short study plan.

The specialist agents are passed to the orchestrator as tools using the Strands Agents SDK's documented Agents-as-Tools pattern.

## Run locally

### 1. Requirements
- Python 3.10+
- Node is not required; the frontend is static HTML/CSS/JS.
- For real AI mode: AWS account, AWS credentials, and access to a supported Amazon Bedrock model in your selected region.

### 2. Backend setup (Windows PowerShell)
```powershell
cd backend
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app:app --reload
```

### 3. Open the app
Open `frontend/index.html` in a browser, or serve the frontend:
```powershell
cd frontend
py -m http.server 5500
```
Then visit `http://localhost:5500`.

### 4. Enable real Strands + Amazon Bedrock mode
In `backend/.env`:
```env
DEMO_MODE=false
AWS_DEFAULT_REGION=us-west-2
```
Configure credentials using `aws configure` or your preferred secure AWS credential method. Enable model access in Amazon Bedrock. Do not commit credentials or `.env` to GitHub.

The API will use the default Bedrock model configured by Strands. If your account uses a different model/region, configure a compatible Bedrock model in `backend/agents.py`.

## API
- `GET /api/health` — backend status and mode
- `POST /api/learn` — body: `{"question":"Explain binary search","subject":"Computer Science","level":"beginner","language":"English","task":"auto"}`

## Important limitations before a public launch
This is a hackathon starter implementation, not a production learning platform. It does not yet authenticate users, persist student records, parse uploaded course files, or independently verify curriculum-specific answers. For a competition submission, test it with real course material, add evaluation examples, and clearly disclose the limits of generated answers.

## Hackathon submission checklist
- [ ] Complete the required Builder Center workshop during the hackathon window.
- [ ] Run and test real Strands mode with Bedrock.
- [ ] Add screenshots and measured evaluation results (do not invent impact metrics).
- [ ] Publish this source code in a public GitHub repository.
- [ ] Record a public demo video under 3 minutes.
- [ ] Publish a Builder Center project article.
- [ ] Confirm the hackathon's current deadline and eligibility rules before submission.

## Suggested evaluation
Create a small test set of 20 questions across 2–3 subjects. Ask instructors or knowledgeable reviewers to rate: correctness, clarity, level adaptation, usefulness of feedback, and whether the study plan targets the learner's actual mistakes. Report the sample size and method honestly.
