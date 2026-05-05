import os
from dotenv import load_dotenv

# Cargamos el archivo .env desde el nivel superior
load_dotenv(dotenv_path="../.env")
load_dotenv() # Por si también hay un .env local

JWT_SECRET = os.getenv("JWT_SECRET")
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")
OLLAMA_ANALYZER_HOST = os.getenv("OLLAMA_ANALYZER_HOST")
OLLAMA_SUMMARIZER_HOST = os.getenv("OLLAMA_SUMMARIZER_HOST")

