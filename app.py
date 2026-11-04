import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

load_dotenv(Path(__file__).with_name(".env"))
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"

app = FastAPI(title="EduSwarm AI API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict to your deployed frontend origin before production.
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

class LearnRequest(BaseModel):
    question: str = Field(min_length=3, max_length=4000)
    subject: str = Field(default="General", max_length=100)
    level: str = Field(default="beginner", max_length=50)
    language: str = Field(default="English", max_length=30)
    task: str = Field(default="auto", max_length=30)

class LearnResponse(BaseModel):
    answer: str
    mode: str
    agents: list[str]

def demo_answer(req: LearnRequest) -> str:
    topic = req.question.strip()
    if req.task == "quiz":
        return (
            f"## Practice set: {req.subject}\n\n"
            f"Topic: **{topic}**\n\n"
            "1. Explain the main idea in your own words.\n"
            "2. Give one real-world example.\n"
            "3. What is one common mistake a beginner might make?\n\n"
            "**Self-check:** Compare your answers with your course notes. "
            "This is a demo response; connect Amazon Bedrock to generate tailored questions."
        )
    if req.task == "plan":
        return (
            f"## Your 3-step learning plan\n\n"
            f"**Topic:** {topic}\n\n"
            "1. **Understand:** Read or review the core definition for 10 minutes.\n"
            "2. **Practice:** Solve two easy examples, then one slightly harder example.\n"
            "3. **Reflect:** Write down what confused you and retry one question tomorrow.\n\n"
            "This is a demo plan. Real mode uses EduSwarm's Learning Coach Agent."
        )
    return (
        f"## Let's learn: {topic}\n\n"
        f"**Subject:** {req.subject} · **Level:** {req.level}\n\n"
        "### 1. Start with the core idea\n"
        f"Break **{topic}** into a definition, why it matters, and one small example.\n\n"
        "### 2. Try explaining it\n"
        "Write a two-sentence explanation without looking at your notes.\n\n"
        "### 3. Check your understanding\n"
        "Create one example and one non-example, then compare them.\n\n"
        "**Demo mode:** This sample response demonstrates the product flow. "
        "Set `DEMO_MODE=false` and configure Amazon Bedrock to activate the real "
        "Strands multi-agent team."
    )

@app.get("/api/health")
def health():
    return {"status": "ok", "mode": "demo" if DEMO_MODE else "strands-bedrock"}

@app.post("/api/learn", response_model=LearnResponse)
def learn(req: LearnRequest):
    prompt = (
        f"Student request: {req.question}\n"
        f"Subject: {req.subject}\nLevel: {req.level}\n"
        f"Response language: {req.language}\nRequested task: {req.task}.\n"
        "Help the learner and use your specialist agents as appropriate."
    )
    if DEMO_MODE:
        return LearnResponse(
            answer=demo_answer(req),
            mode="demo",
            agents=["Tutor Agent", "Quiz Agent", "Learning Coach Agent"],
        )
    try:
        from agents import run_learning_request
        answer = run_learning_request(prompt)
        return LearnResponse(
            answer=answer,
            mode="strands-bedrock",
            agents=["Orchestrator", "Tutor Agent", "Quiz Agent", "Learning Coach Agent"],
        )
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Strands/Bedrock request failed. Check AWS credentials, model access, and region."
        ) from exc
