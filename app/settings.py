from pydantic_settings import BaseSettings, SettingsConfigDict
import os



class Settings(BaseSettings):
    
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DB_PASSWORD: str
    DB_NAME: str
    DB_USERNAME: str
    DB_PORT: str
    DB_HOST: str

    model_config = SettingsConfigDict(env_file='.env')

  


setting = Settings()
