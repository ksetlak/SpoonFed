from sqlalchemy.ext.asyncio import create_async_engine

from config import settings


# dialect+DBAPI
def connect_db():
    engine = create_async_engine(settings.database_url, echo=True)
    return engine
