import os
import io
import uuid
import requests
import json
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydub import AudioSegment
from dotenv import load_dotenv
import dropbox

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Ensure the static directory exists
os.makedirs("static", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Dropbox configuration
DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")
MODELSLAB_API_KEY = os.getenv("MODELSLAB_API_KEY")

dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

# Function to convert the sample rate to 16000 Hz if needed
def convert_sample_rate(audio_bytes):
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
    if audio.frame_rate != 16000:
        audio = audio.set_frame_rate(16000)
    return audio

# Function to upload a file to Dropbox and return its public URL
def upload_file_to_dropbox(file_bytes, file_name):
    response = dbx.files_upload(file_bytes, f"/{file_name}")
    shared_link = dbx.sharing_create_shared_link(path=response.path_display)
    return shared_link.url.replace("dl=0", "raw=1")

# Function to call the ModelsLab API for text-to-speech using cloned voice
def text_to_speech_with_cloned_voice(init_audio_url, text):
    url = "https://modelslab.com/api/v6/voice/text_to_audio"
    payload = json.dumps({
        "key": MODELSLAB_API_KEY,
        "prompt": text,
        "init_audio": init_audio_url,
        "language": "english",
        "webhook": None,
        "track_id": None
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload)
    response.raise_for_status()
    return response.json()

# Endpoint to handle audio file uploads, cloning, and TTS
@app.post("/clone/")
async def clone_audio_file(file: UploadFile = File(...)):
    try:
        audio_bytes = await file.read()
        converted_audio = convert_sample_rate(audio_bytes)

        # Generate a unique file name
        file_id = str(uuid.uuid4())
        dropbox_file_name = f"{file_id}.wav"

        # Upload the file to Dropbox directly from memory and get its public URL
        init_audio_url = upload_file_to_dropbox(converted_audio.export(format='wav').read(), dropbox_file_name)

        # Paragraph to be spoken by the cloned voice
        paragraph = "Hello, how does it feel hearing a clone of your own voice?"

        # Generate TTS audio with the cloned voice
        tts_response = text_to_speech_with_cloned_voice(init_audio_url, paragraph)
        
        # Check the response format and extract the URL
        if tts_response['status'] == 'success' and 'output' in tts_response:
            tts_audio_url = tts_response['output'][0]
        else:
            raise Exception("The TTS API response does not contain the expected 'output'.")

        return JSONResponse(content={"audio_url": tts_audio_url}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Main endpoint to serve the HTML page
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
