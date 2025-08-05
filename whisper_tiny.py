import os
import shutil
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from jiwer import wer, cer
import torch
from transformers import pipeline
import ffmpeg

app = FastAPI()
templates = Jinja2Templates(directory="templates")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load Hugging Face Whisper tiny ASR pipeline
asr = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-tiny",
    device=0 if torch.cuda.is_available() else -1,
)

def convert_to_wav(input_path: str) -> str:
    if input_path.lower().endswith(".wav"):
        return input_path
    output_path = os.path.splitext(input_path)[0] + ".wav"
    (
        ffmpeg
        .input(input_path)
        .output(output_path, ar=16000, ac=1)
        .run(overwrite_output=True)
    )
    os.remove(input_path)
    return output_path

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/", response_class=HTMLResponse)
async def handle_upload(
    request: Request,
    audio: UploadFile = File(...),
    actual_text: str = Form(...),
    language: str = Form("urdu")
):
    # Save uploaded file
    saved_path = os.path.join(UPLOAD_FOLDER, audio.filename)
    with open(saved_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    # Convert to wav with proper specs
    wav_path = convert_to_wav(saved_path)

    # Transcribe with forced Urdu language and transcribe task
    transcription_result = asr(
        wav_path,
        generate_kwargs={"language": language, "task": "transcribe"}
    )
    transcription = transcription_result.get("text", "").strip()

    # Calculate WER and CER
    actual_clean = actual_text.strip()
    wer_score = wer(actual_clean, transcription) * 100
    cer_score = cer(actual_clean, transcription) * 100

    result = {
        "actual": actual_text,
        "transcribed": transcription,
        "wer": round(wer_score, 2),
        "cer": round(cer_score, 2)
    }

    return templates.TemplateResponse("index.html", {"request": request, "result": result})
