from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    MODEL: str = 'gpt-4o-mini'
    EMBEDDING_MODEL: str = 'text-embedding-3-large'
    EMBEDDING_DIMENSIONS: int = 1024
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
    DOCS_DIR: str = 'data/docs'

    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()