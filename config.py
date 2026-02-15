import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_OWNER = "nagapplications"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
