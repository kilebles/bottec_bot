from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str
    WEBHOOK_URL: str
    
    model_config = SettingsConfigDict(env_file=".env")
    

config = Settings()  # type: ignore