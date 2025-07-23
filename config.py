import os
from typing import Optional
from pathlib import Path

env_file = Path(".env")
if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

class Config:
    
    VOXTRAL_API_KEY: str = os.getenv("VOXTRAL_API_KEY", "EMPTY")
    VOXTRAL_API_BASE: str = os.getenv("VOXTRAL_API_BASE", "http://localhost:8000/v1")
    
    # Model Configuration
    MODEL_NAME: str = os.getenv("VOXTRAL_MODEL_NAME", "voxtral-mini-3b-2507")
    
    # Default Parameters
    DEFAULT_TEMPERATURE: float = 0.2
    DEFAULT_TOP_P: float = 0.95
    
    # Audio Configuration
    MAX_AUDIO_SIZE_MB: int = 100
    SUPPORTED_AUDIO_FORMATS: list = ['mp3', 'wav', 'm4a', 'flac', 'ogg']
    
    # Supported Languages
    SUPPORTED_LANGUAGES: list = [
        "English", "Spanish", "French", "German", "Italian", "Portuguese", 
        "Russian", "Chinese", "Japanese", "Korean", "Arabic", "Hindi"
    ]
    
    # UI Configuration
    STREAMLIT_THEME: dict = {
        "primaryColor": "#1f77b4",
        "backgroundColor": "#ffffff",
        "secondaryBackgroundColor": "#f0f2f6",
        "textColor": "#262730",
        "font": "sans serif"
    }
    
    @classmethod
    def get_api_config(cls) -> dict:
        """Get API configuration dictionary"""
        return {
            "api_key": cls.VOXTRAL_API_KEY,
            "base_url": cls.VOXTRAL_API_BASE,
            "model_name": cls.MODEL_NAME
        }
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration settings"""
        if not cls.VOXTRAL_API_BASE:
            return False
        return True
    
    @classmethod
    def get_language_code(cls, language_name: str) -> Optional[str]:
        """Get language code for a given language name"""
        language_mapping = {
            "English": "en",
            "Spanish": "es", 
            "French": "fr",
            "German": "de",
            "Italian": "it",
            "Portuguese": "pt",
            "Russian": "ru",
            "Chinese": "zh",
            "Japanese": "ja",
            "Korean": "ko",
            "Arabic": "ar",
            "Hindi": "hi"
        }
        return language_mapping.get(language_name) 