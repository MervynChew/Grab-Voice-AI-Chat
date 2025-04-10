from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import whisper  # Import the local whisper model
from tempfile import NamedTemporaryFile
from pydub import AudioSegment

# Initialize FastAPI app
app = FastAPI()

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
async def transcribe_audio(file: UploadFile = File(...)):


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

        # Transcribe the audio using the local Whisper model
        result = model.transcribe(wav_file_path)

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

