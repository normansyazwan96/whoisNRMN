import os

import chromadb
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name="resume")


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "status": "RAG chatbot backend is running"
    }


@app.post("/chat")
async def chat(request: ChatRequest):

    # Search the resume for relevant information
    results = collection.query(
        query_texts=[request.question],
        n_results=5
    )

    documents = results.get("documents", [[]])[0]

    # Combine retrieved resume chunks
    context = "\n\n".join(documents)

    prompt = f"""
You are an AI assistant for Norman's professional portfolio.

You must answer the user's question ONLY using the information
provided in the resume context below.

RESUME CONTEXT:
{context}

STRICT RULES:
- Only use information contained in the resume context.
- Do not use outside knowledge.
- Do not invent qualifications, experience, projects, skills,
  certifications, employers or achievements.
- If the answer cannot be found in the resume context, say:
  "I don't have that information in Norman's resume."
- Be professional, concise and friendly.

USER QUESTION:
{request.question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return {
        "answer": response.text
    }