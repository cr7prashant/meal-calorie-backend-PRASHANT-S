from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator
from typing import List, Union

class Settings(BaseSettings):
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Meal Calorie Counter API"
    
    # Database - Simple SQLite URL
    DATABASE_URL: str = "sqlite:///./meal_calorie.db"
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # External APIs
    USDA_API_KEY: str = "NU9KmNNx7iQ48sInhmjOpxo8g0rqd6FhbedfrRcA"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()