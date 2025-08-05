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

# Load Hugging Face Whisper base ASR pipeline
asr = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-base",
    device=0 if torch.cuda.is_available() else -1,
)

def convert_to_wav(input_path: str) -> str:
    """
    If the file is already a mono 16kHz WAV file, return as-is.
    Otherwise, convert to 16kHz mono WAV using ffmpeg.
    """
    if input_path.lower().endswith(".wav"):
        try:
            probe = ffmpeg.probe(input_path)
            stream = next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)
            if stream and int(stream['sample_rate']) == 16000 and int(stream['channels']) == 1:
                return input_path  # Already suitable
        except Exception as e:
            print(f"ffmpeg probe failed: {e}")

    # Convert to 16kHz mono WAV
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
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

    # Convert to proper WAV format if needed
    wav_path = convert_to_wav(saved_path)

    # Transcribe with specified language
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
