import requests
from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
load_dotenv()
app = FastAPI()

class AskRequest(BaseModel):
    url: str
    page_text: str
    question: str



app = FastAPI()

origins = [
    "chrome-extension://pdckaconfphelloaggfhlnbjpbfekaof",  # replace with your actual extension ID
    "http://localhost",  # if you test locally
    "https://chrome-chat-assistant.onrender.com",  # your deployed API (optional for CORS if backend calls only)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # restrict to specified origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ask")
async def ask(req: AskRequest):
    combined_input = f"""
Website URL: {req.url}
Website Content: {req.page_text[:4000]}
User Question: {req.question}

Please provide a helpful, concise answer.
"""

    GROQ_API_KEY = os.getenv("GROQ_API_KEY") # replace with your real key
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "user", "content": combined_input}
            ],
            "temperature": 0.3
        }
    )

    if not response.ok:
        return {"error": f"Groq API error {response.status_code}", "details": response.text}

    result = response.json()
    answer = result["choices"][0]["message"]["content"]
    return {"answer": answer}
