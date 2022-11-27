from pydantic import BaseSettings

class Settings(BaseSettings):
    db_hostname: str
    db_port: str
    db_dbname: str
    db_username: str
    db_password: str

    jwt_secretkey: str
    jwt_algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()

