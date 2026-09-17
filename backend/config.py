from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db_name: str = "expense_intelligence"

    jwt_secret_key: str = "dev_secret_change_me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440

    gemini_api_key: str = ""

    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
