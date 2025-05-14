from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "mistral-nemo"
    EMBEDING_MODEL: str = "nomic-embed-text"
    VECTORSTORE_DESCRIPTION: str = "Vector store about world of warcraft"



settings = Settings()
