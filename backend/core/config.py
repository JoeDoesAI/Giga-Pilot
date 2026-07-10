import os
from dotenv import load_dotenv


load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    HASHING_ALGORITHM: str = os.getenv("HASHING_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES:str = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    ACCESS_CODE:str = os.getenv("ACCESS_CODE")

    #LLM API KEY
    GROQ_API_KEY:str = os.getenv("GROQ_API_KEY")

    # Model Settings
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL")
    EMBEDDING_API_KEY: str = os.getenv("EMBEDDING_API_KEY")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY")


    #file storage settings
    SUPABASE_URL:str = os.getenv("SUPABASE_URL")
    SUPABASE_KEY:str = os.getenv("SUPABASE_KEY")
    SUPABASE_BUCKET:str = os.getenv("SUPABASE_BUCKET")

    SLACK_BOT_TOKEN:str = os.getenv("SLACK_BOT_TOKEN")
    SLACK_SIGNING_SECRET:str = os.getenv("SLACK_SIGNING_SECRET")
    SLACK_APP_TOKEN:str = os.getenv("SLACK_APP_TOKEN")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
  