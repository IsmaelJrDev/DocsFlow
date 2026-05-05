import os
from dotenv import load_dotenv

# Cargamos el archivo .env desde el nivel superior
load_dotenv(dotenv_path="../.env")
load_dotenv() # Por si también hay un .env local

JWT_SECRET = os.getenv("JWT_SECRET", "default_secret")
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user_service:3002")
OLLAMA_ANALYZER_HOST = os.getenv("OLLAMA_ANALYZER_HOST", "http://192.168.1.10:11434")
