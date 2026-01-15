from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
from services.translation_service import TranslationService
from services.chat_service import ChatService
from services.voice_service import VoiceService
from config.settings import settings

app = FastAPI(
    title="Multilingual AI Translation API",
    description="80+ languages support with voice translation",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
translation_service = TranslationService()
chat_service = ChatService()
voice_service = VoiceService()

# Request/Response Models
class TranslationRequest(BaseModel):
    text: str
    source_language: str
    target_language: str

class ChatRequest(BaseModel):
    message: str
    language: str
    conversation_id: Optional[str] = None
    agent_type: Optional[str] = "general"

class VoiceTranslationRequest(BaseModel):
    source_language: str
    target_language: str
    voice_type: Optional[str] = "alloy"

@app.get("/")
async def root():
    return {
        "message": "Multilingual AI Translation API",
        "features": [
            "Text translation in 80+ languages",
            "Voice-to-voice translation",
            "Multilingual chat with AI agents"
        ]
    }

@app.get("/languages")
async def get_supported_languages():
    """Get list of all supported languages"""
    return {
        "supported_languages": translation_service.get_supported_languages(),
        "total_count": len(translation_service.get_supported_languages())
    }

@app.post("/translate")
async def translate_text(request: TranslationRequest):
    """Translate text from one language to another"""
    try:
        result = await translation_service.translate(
            text=request.text,
            source_lang=request.source_language,
            target_lang=request.target_language
        )
        return {
            "success": True,
            "original_text": request.text,
            "translated_text": result,
            "source_language": request.source_language,
            "target_language": request.target_language
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat_with_agent(request: ChatRequest):
    """Chat with AI agent in any language"""
    try:
        response = await chat_service.chat(
            message=request.message,
            language=request.language,
            conversation_id=request.conversation_id,
            agent_type=request.agent_type
        )
        return {
            "success": True,
            "response": response["message"],
            "conversation_id": response["conversation_id"],
            "language": request.language
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/voice/translate")
async def voice_to_voice_translation(
    audio_file: UploadFile = File(...),
    source_language: str = "auto",
    target_language: str = "en",
    voice_type: str = "alloy"
):
    """Voice-to-voice translation"""
    try:
        # Read audio file
        audio_data = await audio_file.read()
        
        # Process voice translation
        result = await voice_service.voice_to_voice_translate(
            audio_data=audio_data,
            source_lang=source_language,
            target_lang=target_language,
            voice_type=voice_type
        )
        
        return {
            "success": True,
            "transcribed_text": result["transcribed_text"],
            "translated_text": result["translated_text"],
            "audio_url": result["audio_url"],
            "source_language": source_language,
            "target_language": target_language
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/voice/transcribe")
async def transcribe_audio(
    audio_file: UploadFile = File(...),
    language: str = "auto"
):
    """Transcribe audio to text"""
    try:
        audio_data = await audio_file.read()
        result = await voice_service.transcribe(audio_data, language)
        return {
            "success": True,
            "transcribed_text": result,
            "language": language
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/voice/synthesize")
async def synthesize_speech(
    text: str,
    language: str = "en",
    voice_type: str = "alloy"
):
    """Convert text to speech"""
    try:
        audio_url = await voice_service.text_to_speech(text, language, voice_type)
        return {
            "success": True,
            "text": text,
            "audio_url": audio_url,
            "language": language,
            "voice_type": voice_type
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)