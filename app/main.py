from typing import Dict

import sqlalchemy as sa
from fastapi import FastAPI
from pydantic import EmailStr
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from app.config import settings
from app.tables import user

app = FastAPI()
engine: AsyncEngine = create_async_engine(settings.PG_DSN)
session = AsyncSession(engine)


@app.get("/ping")
def ping() -> str:
    return "pong"


@app.post("/users")
async def create_user(username: str, email: EmailStr) -> Dict[str, int]:
    async with session:
        query = (
            sa.insert(user)
            .values({"username": username, "email": email})
            .returning(user.c.id)
        )
        result: CursorResult = await session.execute(query)
    return {"id": result.one()[0]}
