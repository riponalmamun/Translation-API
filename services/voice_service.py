import openai
from config.settings import settings
from typing import Dict
import tempfile
import os
from pathlib import Path

class VoiceService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.audio_dir = Path("audio_files")
        self.audio_dir.mkdir(exist_ok=True)
    
    async def transcribe(self, audio_data: bytes, language: str = "auto") -> str:
        """Transcribe audio to text using Whisper API"""
        try:
            # Save audio temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                temp_audio.write(audio_data)
                temp_audio_path = temp_audio.name
            
            # Transcribe using Whisper
            with open(temp_audio_path, "rb") as audio_file:
                if language == "auto":
                    transcript = openai.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file
                    )
                else:
                    transcript = openai.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        language=language
                    )
            
            # Clean up temp file
            os.unlink(temp_audio_path)
            
            return transcript.text
            
        except Exception as e:
            if os.path.exists(temp_audio_path):
                os.unlink(temp_audio_path)
            raise Exception(f"Transcription error: {str(e)}")
    
    async def text_to_speech(
        self, 
        text: str, 
        language: str = "en", 
        voice_type: str = "alloy"
    ) -> str:
        """Convert text to speech using OpenAI TTS"""
        try:
            # Available voices: alloy, echo, fable, onyx, nova, shimmer
            response = openai.audio.speech.create(
                model="tts-1",
                voice=voice_type,
                input=text
            )
            
            # Save audio file
            audio_filename = f"speech_{hash(text)}.mp3"
            audio_path = self.audio_dir / audio_filename
            
            with open(audio_path, "wb") as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)
            
            # Return file path or URL
            return str(audio_path)
            
        except Exception as e:
            raise Exception(f"Text-to-speech error: {str(e)}")
    
    async def voice_to_voice_translate(
        self,
        audio_data: bytes,
        source_lang: str,
        target_lang: str,
        voice_type: str = "alloy"
    ) -> Dict:
        """Complete voice-to-voice translation pipeline"""
        try:
            # Step 1: Transcribe audio to text
            transcribed_text = await self.transcribe(audio_data, source_lang)
            
            # Step 2: Translate text
            from services.translation_service import TranslationService
            translator = TranslationService()
            
            # Auto-detect source language if needed
            if source_lang == "auto":
                source_lang = await translator.detect_language(transcribed_text)
            
            translated_text = await translator.translate(
                text=transcribed_text,
                source_lang=source_lang,
                target_lang=target_lang
            )
            
            # Step 3: Convert translated text to speech
            audio_url = await self.text_to_speech(
                text=translated_text,
                language=target_lang,
                voice_type=voice_type
            )
            
            return {
                "transcribed_text": transcribed_text,
                "translated_text": translated_text,
                "audio_url": audio_url
            }
            
        except Exception as e:
            raise Exception(f"Voice-to-voice translation error: {str(e)}")