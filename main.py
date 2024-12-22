#pip install fastapi/uvicorn/pydantic
from fastapi import FastAPI, HTTPException 
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI ()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database = {
    "verbs": [
        {"verb": "get", "examples": [
            {"english": "I got you covered.", "korean": "내가 널 책임질게."},
            {"english": "I get it.", "korean": "이해했어."},
            {"english": "It got you.", "korean": "그게 널 잡았어."}
        ]},
        {"verb": "bring", "examples": [
            {"english": "Bring me the book.", "korean": "그 책을 가져와."},
            {"english": "Can you bring it to me?", "korean": "그거 나한테 가져다줄래?"},
        ]},
        {"verb": "tell", "examples": [
            {"english": "Tell me the truth.", "korean": "진실을 말해줘."},
            {"english": "I can tell you everything.", "korean": "내가 너한테 다 말해줄게."}
        ]}
    ]
}

class SentenceCheckRequest(BaseModel):
    user_input: str
    correct_sentence: str

@app.get("/verbs")
def get_verbs():
    return [verb["verb"] for verb in database["verbs"]]

@app.get("/examples/{verb}")
def get_examples(verb: str):
    for entry in database["verbs"]:
        if entry["verb"] == verb:
            return entry["examples"]
    raise HTTPException(status_code=404, detail="Verb not found")

@app.post("/check_sentence")
def check_sentence(request: SentenceCheckRequest):
    is_correct = request.user_input.strip().lower() == request.correct_sentence.strip().lower()
    return {"is_correct": is_correct}