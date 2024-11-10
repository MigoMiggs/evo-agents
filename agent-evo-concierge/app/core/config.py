from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # Basic API Config
    PROJECT_NAME: str = "Evo Concierge Agent"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Server Config
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    
    # Add any additional configuration settings here
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 