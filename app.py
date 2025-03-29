from fastapi import FastAPI, UploadFile, File
import requests
from io import BytesIO
from fastapi.responses import StreamingResponse, HTMLResponse
import PyPDF2
import os

app = FastAPI()

# Serve static files (including HTML)
@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    with open("static/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

# Eleven Labs API setup
API_KEY = "YOUR_ELEVEN_LABS_API_KEY"
URL = "https://api.elevenlabs.io/synthesize"

@app.get("/speak/")
def generate_speech_elevenlabs(text: str):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
    }
    data = {
        "text": text,
        "voice": "en_us_male",  # You can choose different voices (male/female)
    }
    
    response = requests.post(URL, json=data, headers=headers)
    
    if response.status_code == 200:
        audio_content = response.content
        audio_buffer = BytesIO(audio_content)
        audio_buffer.seek(0)
        return StreamingResponse(audio_buffer, media_type="audio/mpeg")
    else:
        return {"error": "Could not generate speech."}

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    pdf_reader = PyPDF2.PdfReader(file.file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + " "
    
    if not text.strip():
        return {"error": "Could not extract text from PDF."}
    
    return generate_speech_elevenlabs(text)

# Ensure the app runs on the correct port
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Default to 8000 if PORT is not set
    uvicorn.run(app, host="0.0.0.0", port=port)
