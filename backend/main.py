import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "chroma_db"

load_dotenv(BASE_DIR / ".env")

app = FastAPI(title="normAI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://floweaver.top",
        "https://www.floweaver.top",
        "https://whoisnrmn.pages.dev",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

chroma_client = chromadb.PersistentClient(path=str(DB_PATH))
try:
    collection = chroma_client.get_collection(name="resume")
except Exception:
    collection = None


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)


@app.get("/")
def root():
    return {"status": "normAI backend is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
def ready():
    if client is None:
        raise HTTPException(status_code=503, detail="GEMINI_API_KEY is not configured.")
    if collection is None:
        raise HTTPException(status_code=503, detail="Resume collection is not available. Run ingest.py.")
    return {"status": "ready"}


@app.post("/chat")
async def chat(request: ChatRequest):
    if client is None:
        raise HTTPException(status_code=503, detail="AI service is not configured.")
    if collection is None:
        raise HTTPException(status_code=503, detail="Knowledge base is not available.")

    try:
        results = collection.query(query_texts=[request.question.strip()], n_results=5)
        documents = results.get("documents", [[]])[0]
        context = "\n\n".join(documents)

        if not context.strip():
            return {"answer": "I don't have that information in Norman's resume."}

        prompt = f"""
You are normAI, the AI assistant for Norman Syazwan's professional portfolio.

Answer the user's question ONLY using the resume context below.

RESUME CONTEXT:
{context}

STRICT RULES:
- Only use information contained in the resume context.
- Do not use outside knowledge.
- Do not invent qualifications, experience, projects, skills, certifications, employers, or achievements.
- If the answer cannot be found in the resume context, say:
  "I don't have that information in Norman's resume."
- Be professional, concise, and friendly.

USER QUESTION:
{request.question}
"""

        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        answer = getattr(response, "text", None)
        if not answer:
            raise HTTPException(status_code=502, detail="AI service returned an empty response.")
        return {"answer": answer}

    except HTTPException:
        raise
    except Exception as exc:
        print(f"normAI chat error: {exc}")
        raise HTTPException(status_code=500, detail="Unable to process the request right now.") from exc
