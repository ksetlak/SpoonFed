from sqlalchemy.ext.asyncio import create_async_engine


# engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
# dialect+DBAPI
def connect_db():
    # TODO: Will need config management of course.
    engine = create_async_engine("postgresql+asyncpg://postgres:mysecretpassword@localhost:5432", echo=True)
    return engine
