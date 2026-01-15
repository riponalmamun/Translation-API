import openai
from config.settings import settings
from typing import Dict, List

class TranslationService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.supported_languages = self._load_supported_languages()
    
    def _load_supported_languages(self) -> Dict[str, str]:
        """Load all supported languages"""
        return {
            "en": "English", "es": "Spanish", "fr": "French", "de": "German",
            "it": "Italian", "pt": "Portuguese", "ru": "Russian", "ja": "Japanese",
            "ko": "Korean", "zh": "Chinese", "ar": "Arabic", "hi": "Hindi",
            "bn": "Bengali", "ur": "Urdu", "id": "Indonesian", "tr": "Turkish",
            "vi": "Vietnamese", "th": "Thai", "pl": "Polish", "nl": "Dutch",
            "sv": "Swedish", "da": "Danish", "no": "Norwegian", "fi": "Finnish",
            "cs": "Czech", "hu": "Hungarian", "ro": "Romanian", "el": "Greek",
            "he": "Hebrew", "fa": "Persian", "uk": "Ukrainian", "bg": "Bulgarian",
            "sr": "Serbian", "hr": "Croatian", "sk": "Slovak", "sl": "Slovenian",
            "lt": "Lithuanian", "lv": "Latvian", "et": "Estonian", "is": "Icelandic",
            "ga": "Irish", "mt": "Maltese", "cy": "Welsh", "eu": "Basque",
            "ca": "Catalan", "gl": "Galician", "af": "Afrikaans", "sq": "Albanian",
            "az": "Azerbaijani", "be": "Belarusian", "bs": "Bosnian", "ka": "Georgian",
            "hy": "Armenian", "mk": "Macedonian", "mn": "Mongolian", "kk": "Kazakh",
            "uz": "Uzbek", "sw": "Swahili", "ha": "Hausa", "yo": "Yoruba",
            "ig": "Igbo", "am": "Amharic", "so": "Somali", "ny": "Chichewa",
            "mg": "Malagasy", "mi": "Maori", "sm": "Samoan", "haw": "Hawaiian",
            "ms": "Malay", "tl": "Tagalog", "jv": "Javanese", "su": "Sundanese",
            "lo": "Lao", "my": "Burmese", "km": "Khmer", "ne": "Nepali",
            "si": "Sinhala", "ta": "Tamil", "te": "Telugu", "ml": "Malayalam",
            "kn": "Kannada", "mr": "Marathi", "gu": "Gujarati", "pa": "Punjabi",
            "sd": "Sindhi", "ps": "Pashto", "ku": "Kurdish", "ckb": "Central Kurdish"
        }
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Return all supported languages"""
        return self.supported_languages
    
    async def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate text using GPT API"""
        try:
            # Validate languages
            if source_lang not in self.supported_languages:
                raise ValueError(f"Unsupported source language: {source_lang}")
            if target_lang not in self.supported_languages:
                raise ValueError(f"Unsupported target language: {target_lang}")
            
            # Create translation prompt
            prompt = f"""Translate the following text from {self.supported_languages[source_lang]} to {self.supported_languages[target_lang]}.
Only provide the translation, nothing else.

Text to translate: {text}

Translation:"""
            
            # Call OpenAI API
            response = openai.chat.completions.create(
                model=settings.GPT_MODEL,
                messages=[
                    {"role": "system", "content": "You are a professional translator. Provide accurate translations preserving the tone and meaning."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            translated_text = response.choices[0].message.content.strip()
            return translated_text
            
        except Exception as e:
            raise Exception(f"Translation error: {str(e)}")
    
    async def detect_language(self, text: str) -> str:
        """Detect the language of given text"""
        try:
            prompt = f"""Detect the language of the following text. Reply with only the ISO 639-1 language code (e.g., 'en', 'es', 'fr').

Text: {text}

Language code:"""
            
            response = openai.chat.completions.create(
                model=settings.GPT_MODEL,
                messages=[
                    {"role": "system", "content": "You are a language detection system. Reply only with the ISO 639-1 language code."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=10
            )
            
            language_code = response.choices[0].message.content.strip().lower()
            return language_code
            
        except Exception as e:
            raise Exception(f"Language detection error: {str(e)}")