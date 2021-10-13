import os
from pydantic import BaseSettings, Field
from functools import lru_cache

os.environ["CQLENG_ALLOW_SCHEMA_MANAGEMENT"] = "1"
class Settings(BaseSettings):
    bucket_name: str = Field(..., env="BUCKET_NAME")
    db_client_id: str = Field(..., env="ASTRA_DB_CLIENT_ID")
    db_client_secret: str = Field(..., env="ASTRA_DB_CLIENT_SECRET")

    class Config:
        env_file = '.env'
        
@lru_cache
def get_settings():
    settings = Settings()
    return settings
