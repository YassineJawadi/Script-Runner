import os
from dotenv import load_dotenv
from .services.ollama_client import prewarm_model

# load .env file
load_dotenv()

from . import create_app

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"

    app = create_app()
    prewarm_model("Warm up")
    app.run(host=host, port=port, debug=debug)
