from fastapi import FastAPI, UploadFile, File
from gtts import gTTS
from io import BytesIO
from fastapi.responses import StreamingResponse
import PyPDF2
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Text-to-Speech API!"}

@app.get("/speak/")
def generate_speech(text: str):
    tts = gTTS(text, lang="en", slow=False)
    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return StreamingResponse(audio_buffer, media_type="audio/mpeg")

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    pdf_reader = PyPDF2.PdfReader(file.file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + " "
    
    if not text.strip():
        return {"error": "Could not extract text from PDF."}
    
    return generate_speech(text)

# Ensure the app runs on the correct port
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Default to 8000 if PORT is not set
    uvicorn.run(app, host="0.0.0.0", port=port)
