from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import whisper  # Import the local whisper model
from tempfile import NamedTemporaryFile
from pydub import AudioSegment

import subprocess  # ⬅ Add this at the top
import uuid  # ⬅ Optional: for generating unique filenames

from .chatbot import ask_chatbot  # <- chatbot function
from pydantic import BaseModel
from typing import List, Dict, Optional # Added List, Dict, Optional

# Define the request format for /chat endpoint
class ChatRequest(BaseModel):
    message: str
    driver_type: str
    chat_history: Optional[List[Dict[str, str]]] = None


# Initialize FastAPI app
app = FastAPI()

@app.get("/")  # Handle GET requests to the root URL
def read_root():
    return {"message": "Welcome to the server!"}

# Add CORS middleware to allow cross-origin requests
# CORS for all localhost and local IP addresses
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ← TEMP fix for testing (open to all origins)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

allow_origins=[
    "http://localhost:19006", 
    "http://127.0.0.1:19006", 
    "http://192.168.100.5:19006"
]


# Load the Whisper model
model = whisper.load_model("base")  # You can change "base" to another model like "small", "medium", etc.

# Endpoint to process audio and get transcription
@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...), language: str = None):


    # print("filename:", file.filename)
    # print("content_type:", file.content_type)
    # return {"message": "received", "filename": file.filename}


    temp_file_path = None
    wav_file_path = None
    try:
        # Save the uploaded audio file temporarily
        with NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name
        
        # Convert the audio file to a format that Whisper can handle (WAV)
        audio = AudioSegment.from_file(temp_file_path)
        wav_file_path = temp_file_path + ".wav"
        audio.export(wav_file_path, format="wav")

        # === Noise Reduction using RNNoise ===
        # Generate temporary filenames
        input_raw_path = wav_file_path + ".raw"
        output_raw_path = wav_file_path + "_denoised.raw"
        denoised_wav_path = wav_file_path.replace(".wav", "_denoised.wav")

        # Path to ffmpeg executable - use from PATH
        ffmpeg_path = r"C:\Users\USER\Documents\UMHakathon\ffmpeg-master-latest-win64-gpl-shared\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe"

        # 1. Convert WAV to raw PCM (s16le, 48kHz, mono)
        subprocess.run([
            ffmpeg_path, "-y", "-i", wav_file_path,
            "-f", "s16le", "-ar", "48000", "-ac", "1", input_raw_path
        ], check=True)

        if not os.path.exists(input_raw_path) or os.path.getsize(input_raw_path) == 0:
            raise Exception("Conversion to raw PCM failed: input.raw is missing or empty.")


        print("filename:", file.filename)

        # 2. Apply RNNoise
        rnnoise_exe = r"C:/Users/USER/RNNoise/rnnoise/examples/rnnoise_demo.exe"

        try:
            subprocess.run(
                [rnnoise_exe, input_raw_path, output_raw_path],
                check=True,
                cwd=r"C:/Users/USER/RNNoise/rnnoise"
            )
        except subprocess.CalledProcessError as e:
            print("RNNoise execution failed:", e)
            raise Exception("Noise reduction failed.") from e

        print("content_type:", file.content_type)

        if not os.path.exists(output_raw_path) or os.path.getsize(output_raw_path) == 0:
            raise Exception("Noise reduction failed: output.raw is missing or empty.")


        # 3. Convert back to WAV from raw
        subprocess.run([
            ffmpeg_path, "-y", "-f", "s16le", "-ar", "48000", "-ac", "1",
            "-i", output_raw_path, denoised_wav_path
        ], check=True)

        print(f"Temporary file path: {temp_file_path}")
        print(f"WAV file path: {wav_file_path}")
        print(f"Raw PCM path: {input_raw_path}")
        print(f"Denoised output path: {output_raw_path}")
        print(f"Denoised WAV path: {denoised_wav_path}")
        print(f"Language: {language}")  # Log the language parameter


        # Transcribe the denoised audio with language specified if provided
        if language:
            result = model.transcribe(denoised_wav_path, language=language)
        else:
            result = model.transcribe(denoised_wav_path)

        # Return the transcription result
        return JSONResponse(content={"transcription": result['text']})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    finally:
        # Clean up the temporary files
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        if wav_file_path and os.path.exists(wav_file_path):
            os.remove(wav_file_path)
        if input_raw_path and os.path.exists(input_raw_path):
            os.remove(input_raw_path)
        if output_raw_path and os.path.exists(output_raw_path):
            os.remove(output_raw_path)


@app.post("/chat")
async def chat_with_bot(request: ChatRequest):
    try:
        history = request.chat_history if request.chat_history is not None else []
        reply = ask_chatbot(request.message, request.driver_type, history)
        return {"reply": reply}
    except Exception as e:
        print(f"Error in /chat endpoint: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})