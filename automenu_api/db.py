from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from config import settings


# dialect+DBAPI
def init_engine() -> AsyncEngine:
    return create_async_engine(settings.database_url, echo=True)


def get_engine(request: Request) -> AsyncEngine:
    return request.app.state.engine


async def get_db_session(engine: Annotated[AsyncEngine, Depends(get_engine)]) -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        try:
            yield session  # await session.commit() absent on purpose
        except Exception:
            await session.rollback()
            raise
