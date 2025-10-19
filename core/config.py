from pydantic_settings import BaseSettings
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 3


class Settings(BaseSettings):
    sql_db_url: str = os.getenv("SQL_DB_URL")

    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
