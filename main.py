from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import uuid
import subprocess
from pathlib import Path
from models import Recording, UrduText
from database import get_db, engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Voice Recording API", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Directory for uploads
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/")
async def root():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.get("/prompt/{prompt_id}")
async def get_prompt(prompt_id: int, db: Session = Depends(get_db)):
    prompt = db.query(UrduText).filter(UrduText.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return {"id": prompt.id, "text": prompt.content}


@app.get("/prompts")
async def get_all_prompts(db: Session = Depends(get_db)):
    prompts = db.query(UrduText).all()
    return [{"id": p.id, "text": p.content} for p in prompts]


def convert_webm_to_wav(webm_path: Path, wav_path: Path):
    command = [
        "ffmpeg", "-i", str(webm_path),
        "-ar", "16000", "-ac", "1",
        str(wav_path)
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


@app.post("/upload/")
async def upload_recording(
    name: str = Form(...),
    phone_number: str = Form(...),
    prompt_id: int = Form(...),
    audio_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Validate prompt
    prompt = db.query(UrduText).filter(UrduText.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=400, detail="Invalid prompt ID")

    # Validate file extension
    if not audio_file.filename.endswith('.webm'):
        raise HTTPException(status_code=400, detail="Only .webm files are allowed")

    # Create user-specific directory
    user_dir = UPLOAD_DIR / phone_number
    user_dir.mkdir(parents=True, exist_ok=True)

    webm_filename = f"{uuid.uuid4()}.webm"
    webm_path = user_dir / webm_filename

    # Save uploaded file
    with open(webm_path, "wb") as f:
        f.write(await audio_file.read())

    # Convert to WAV
    wav_filename = webm_filename.replace(".webm", ".wav")
    wav_path = user_dir / wav_filename

    try:
        convert_webm_to_wav(webm_path, wav_path)
        webm_path.unlink(missing_ok=True)  # Remove original .webm

        # Save record in database
        recording = Recording(
            name=name,
            phone_number=phone_number,
            prompt_id=prompt_id,
            filename=wav_filename
        )
        db.add(recording)
        db.commit()
        db.refresh(recording)

        return {
            "message": "Recording uploaded and converted",
            "recording_id": recording.id,
            "filename": wav_filename,
            "prompt": prompt.content
        }

    except Exception as e:
        webm_path.unlink(missing_ok=True)
        wav_path.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail=f"Upload failed: {e}")


@app.get("/recordings/{phone_number}")
async def get_user_recordings(phone_number: str, db: Session = Depends(get_db)):
    recordings = db.query(Recording).filter(Recording.phone_number == phone_number).all()
    prompt_map = {p.id: p.content for p in db.query(UrduText).all()}

    return [{
        "id": r.id,
        "name": r.name,
        "prompt_id": r.prompt_id,
        "prompt_text": prompt_map.get(r.prompt_id, "Unknown prompt"),
        "filename": r.filename,
        "created_at": r.created_at
    } for r in recordings]


if __name__ == "__main__":
    app.run(debug=True)
