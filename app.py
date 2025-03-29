import os
from fastapi import FastAPI
from gtts import gTTS
from io import BytesIO
from fastapi.responses import StreamingResponse

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

# Ensure the app runs on the correct port
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Default to 8000 if PORT is not set
    uvicorn.run(app, host="0.0.0.0", port=port)
