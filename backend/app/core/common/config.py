import os
from typing import Optional, Dict, Any
from pydantic import BaseSettings, PostgresDsn, validator


# 공통 설정
class Settings(BaseSettings):

    SWAGGER_TITLE = "SignUp API"

    STAGE: str = os.environ.get("STAGE", "local")

    #######################
    # DATABASE URI 설정
    #######################
    if STAGE == "local":
        POSTGRES_SERVER: str = "host.docker.internal:5431"
        POSTGRES_USER: str = "admin"
        POSTGRES_PASSWORD: str = "admin1234"
        POSTGRES_DB: str = "postgres"
        DB_ECHO: bool = True

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        print("assemble_db_connection.v : ", v)
        print("assemble_db_connection.values : ", values)
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),  # type:ignore
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )


settings = Settings()


# 모듈 테스트
if __name__ == "__main__":
    pass
