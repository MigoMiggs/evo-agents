from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Resume RAG Agent"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    
    # Resume-specific settings
    RESUME_INDEX_PATH: str = os.getenv("RESUME_INDEX_PATH", "data/resume_index")
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 