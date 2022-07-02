from typing import Dict

import sqlalchemy as sa
from fastapi import FastAPI
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.config import settings
from app.tables import user

app = FastAPI(root_path=settings.ROOT_PATH)
engine: AsyncEngine = create_async_engine(settings.PG_DSN)


@app.get("/ping")
def ping() -> str:
    return "pong"


@app.post("/users")
async def create_user(username: str, email: EmailStr) -> Dict[str, int]:
    async with engine.begin() as conn:
        query = (
            sa.insert(user)
            .values({"username": username, "email": email})
            .returning(user.c.id)
        )
        result = await conn.execute(query)
    return {"id": result.one()[0]}
