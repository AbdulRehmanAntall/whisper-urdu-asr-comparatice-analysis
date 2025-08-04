import os
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from pydub import AudioSegment
from jiwer import wer, cer  # <-- import CER here
import shutil
import torch
from transformers import pipeline

app = FastAPI()
templates = Jinja2Templates(directory="templates")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load Hugging Face Whisper tiny ASR pipeline once
asr = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-tiny",
    device=0 if torch.cuda.is_available() else -1,
)

def convert_to_wav(input_path: str) -> str:
    if input_path.lower().endswith(".wav"):
        return input_path
    audio = AudioSegment.from_file(input_path)
    wav_path = os.path.splitext(input_path)[0] + ".wav"
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export(wav_path, format="wav")
    os.remove(input_path)  # remove original non-wav file
    return wav_path

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/", response_class=HTMLResponse)
async def handle_upload(
    request: Request,
    audio: UploadFile = File(...),
    actual_text: str = Form(...),
    language: str = Form("urdu")  # Note: HuggingFace model is multilingual but not perfect for all
):
    # Save uploaded file
    saved_path = os.path.join(UPLOAD_FOLDER, audio.filename)
    with open(saved_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    # Convert to wav with proper specs
    wav_path = convert_to_wav(saved_path)

    # Run Hugging Face whisper tiny transcription
    transcription_result = asr(wav_path)
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
