import os
from typing import Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Try loading from the root of the v2 project
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'),
        env_file_encoding='utf-8',
        extra='ignore'
    )

    # LLM Providers
    groq_api_key: str = Field(..., alias="GROQ_API_KEY")
    gemini_api_key: Optional[str] = Field(None, alias="GEMINI_API_KEY")
    openrouter_api_key: Optional[str] = Field(None, alias="OPENROUTER_API_KEY")

    # Observability & Tracing
    langchain_tracing_v2: bool = Field(False, alias="LANGCHAIN_TRACING_V2")
    langchain_api_key: Optional[str] = Field(None, alias="LANGCHAIN_API_KEY")
    langchain_project: str = Field("jobcrew-v2", alias="LANGCHAIN_PROJECT")
    langchain_endpoint: str = Field("https://api.smith.langchain.com", alias="LANGCHAIN_ENDPOINT")
    sentry_dsn: Optional[str] = Field(None, alias="SENTRY_DSN")

    # Job Sources
    adzuna_app_id: Optional[str] = Field(None, alias="ADZUNA_APP_ID")
    adzuna_api_key: Optional[str] = Field(None, alias="ADZUNA_API_KEY")
    usajobs_api_key: Optional[str] = Field(None, alias="USAJOBS_API_KEY")
    usajobs_user_agent: Optional[str] = Field(None, alias="USAJOBS_USER_AGENT")

    # Database Settings
    supabase_url: Optional[str] = Field(None, alias="SUPABASE_URL")
    supabase_key: Optional[str] = Field(None, alias="SUPABASE_KEY")

    # App General Settings
    environment: str = Field("development", alias="ENVIRONMENT")
    pipeline_version: str = Field("2.0.0", alias="PIPELINE_VERSION")
    request_timeout: float = Field(30.0, alias="REQUEST_TIMEOUT")
    log_level: str = Field("INFO", alias="LOG_LEVEL")

    # Fit Scoring Thresholds
    fit_score_fast_track_threshold: float = Field(8.0, alias="FIT_SCORE_FAST_TRACK_THRESHOLD")
    fit_score_standard_threshold: float = Field(5.0, alias="FIT_SCORE_STANDARD_THRESHOLD")

    # Local & Alternative LLM configs
    ollama_model: str = Field("llama3", alias="OLLAMA_MODEL")
    ollama_base_url: str = Field("http://localhost:11434", alias="OLLAMA_BASE_URL")
    openrouter_model: str = Field("meta-llama/llama-3.1-8b-instruct:free", alias="OPENROUTER_MODEL")

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        valid_envs = ["development", "staging", "production"]
        if v.lower() not in valid_envs:
            raise ValueError(f"ENVIRONMENT must be one of {valid_envs}")
        return v.lower()

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"LOG_LEVEL must be one of {valid_levels}")
        return v.upper()

try:
    settings = Settings()
except Exception as e:
    import sys
    print(f"\n[Configuration Error] Failed to load/validate environment settings:\n{e}\n", file=sys.stderr)
    raise e
