from pydantic import BaseSettings, Field, PostgresDsn


class Settings(BaseSettings):
    PG_DSN: PostgresDsn = Field(
        env="PG_DSN",
        default="postgresql+asyncpg://user:password@db:5432/python_architecture",
    )
    ROOT_PATH: str = Field(env="ROOT_PATH", default="/")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
