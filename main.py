#pip install fastapi/uvicorn/pydantic
from fastapi import FastAPI, Depends, HTTPException 
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, Verb, Example

app = FastAPI ()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/verbs")
def get_verbs(db: Session = Depends(get_db)):
    verbs = db.query(Verb).all()
    if not verbs:
        raise HTTPException(status_code=404, detail="단어를 찾지 못했습니다.")
    return [{"id": verb.id, "verb": verb.verb} for verb in verbs]

@app.get("/examples/{verb}")
def get_examples(verb: str, db: Session = Depends(get_db)):
    verb_entry = db.query(Verb).filter(Verb.verb == verb).first()
    if not verb_entry:
        raise HTTPException(status_code=404, detail="단어를 찾지 못했습니다.")
    return [
        {"english": example.english, "korean": example.korean}
        for example in verb_entry.examples
    ]

#요청 데이터의 모델 정의
class SentenceCheckRequest(BaseModel):
    user_input: str
    correct_sentence: str

@app.post("/check_sentence")
def check_sentence(request: SentenceCheckRequest):
    is_correct = request.user_input.strip().lower() == request.correct_sentence.strip().lower()
    return {"is_correct": is_correct}