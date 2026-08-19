import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

load_dotenv("backend/.env")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://floweaver.top",
"https://www.floweaver.top"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {"status": "Chatbot backend is running"}


@app.post("/chat")
async def chat(request: ChatRequest):

    prompt = f"""
You are an AI assistant for Norman's professional portfolio.

Answer questions about Norman's:
- IT experience
- technical skills
- certifications
- projects
- AI and automation experience
- cloud experience

Be professional, concise and friendly.

Only answer based on information available about Norman.
If you don't know something, say that the information is not available.
Do not invent qualifications, experience or projects.

User question:
{request.question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return {
        "answer": response.text
    }
