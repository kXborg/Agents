import os
from dotenv import load_dotenv

# Load .env ONCE
load_dotenv()

# LLM INITIALIZATION
from langchain_google_genai import ChatGoogleGenerativeAI

LLM = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
)

# config values for the rest of the app
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_API_BASE = "https://api.github.com/repos/"
GITHUB_API_RAW = "https://raw.githubusercontent.com/"

# constants
MAX_SIZE_KB = 500
MAX_CHUNKS = 8  # manageable for prompt length

#lists of constants
EXCLUDE_EXT = [
    ".gif", ".jpg", ".jpeg", ".png", ".mp4",
    ".gitignore", ".git", ".pdf", ".vscode", ".docker",
    ".docstr", ".docstr.yaml", ".github"
]
IMPORTANT_EXT = [".py", ".ipynb", ".md", ".json", ".yaml", ".toml"]
IMPORTANT_NAMES = ["readme", "setup", "main", "__init__", "app", "model", "config"]