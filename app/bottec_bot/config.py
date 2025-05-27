from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str
    WEBHOOK_URL: str
    
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    
    YOOKASSA_ID: int
    YOOKASSA_KEY: str
    
    model_config = SettingsConfigDict(env_file='.env')
    

config = Settings()  # type: ignore