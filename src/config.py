import os
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

class Config:
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen:latest")
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")

    @staticmethod
    def validate():
        if not Config.SERPER_API_KEY:
            raise ValueError("SERPER_API_KEY is missing in .env file")
