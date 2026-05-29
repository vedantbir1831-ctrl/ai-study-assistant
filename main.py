from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
import shutil
import fitz
import os
import logging

from ai_engine import summarize_notes, generate_quiz
from database import SessionLocal, Report
from rag_engine import store_embeddings
from auth import verify_token

app = FastAPI()

logging.basicConfig(level=logging.INFO)
print("🔥 FastAPI app starting...")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token missing")

    try:
        token = authorization.split(" ")[1]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token format")

    payload = verify_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload

@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    user=Depends(get_current_user)
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        pdf = fitz.open(file_path)

        text = ""
        for page in pdf:
            text += page.get_text()

        store_embeddings(text, file.filename)

        summary = summarize_notes(text[:3000])
        quiz = generate_quiz(text[:3000])

        db = SessionLocal()

        report = Report(
            filename=file.filename,
            summary=summary,
            quiz=quiz,
            user_id=user["user_id"]
        )

        db.add(report)
        db.commit()
        db.close()

        return {
            "summary": summary,
            "quiz": quiz
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        file.file.close()