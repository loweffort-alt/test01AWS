import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PRODUCTION_URL = os.getenv("PRODUCTION_URL")
    LOCAL_URL = os.getenv("LOCAL_URL", "http://localhost:8000")
    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
    APP_ENV = os.getenv("APP_ENV", "dev")


settings = Settings()
