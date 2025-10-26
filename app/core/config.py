from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    LLM_API_URL: str = "https://api.mistral.ai/v1/chat/completions"
    LLM_API_KEY: str = "AUgs3e0v5p9qz62dm988uoRppGsQxpma"


settings = Settings()
