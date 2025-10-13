class Config:
    # Hardcoded configuration (no .env)
    OLLAMA_HOST = "http://localhost:11434"
    OLLAMA_API = f"{OLLAMA_HOST}/api/generate"
    OLLAMA_MODEL = "mistral"
    DEFAULT_MAX_TOKENS = 512

    # Flask server settings
    HOST = "0.0.0.0"
    PORT = 5004
    FLASK_DEBUG = True
