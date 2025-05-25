from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str
    WEBHOOK_URL: str
    
    CHANNEL_LINK: str
    CHANNEL_ID: int

    GROUP_LINK: str
    GROUP_ID: int
    
    model_config = SettingsConfigDict(env_file='.env')
    

config = Settings()  # type: ignore