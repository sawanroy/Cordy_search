# config.py

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COMPANY_DATA_DIR = os.path.join(BASE_DIR, "company_data")

# Ollama configuration
OLLAMA_MODEL = "mistral" # change if needed
OLLAMA_URL = "http://localhost:11434/api/generate"

# Search configuration
DUCKDUCKGO_MAX_RESULTS = 10

# General settings
REQUEST_TIMEOUT = 15
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64)"
