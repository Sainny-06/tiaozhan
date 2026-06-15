from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "mvp.sqlite3"
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"

APP_NAME = "智学工坊 MVP"
