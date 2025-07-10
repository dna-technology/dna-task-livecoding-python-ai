from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
    )

    data_dir: Path = Path("data/documents")
    vector_dir: Path = Path("data/vector_store")

    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    model_name: str = "gpt-4o-mini"
    embeddings_model: str = "text-embedding-3-small"

    chunk_size: int = 1_000
    chunk_overlap: int = 100


settings = Settings() 