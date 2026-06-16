from sqlalchemy import create_engine


# engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
# dialect+DBAPI from the tutorial: postgresql+psycopg2; Turns out that's the go-to.
# For prod we will need deps: RUN apt-get update && apt-get install -y libpq-dev; RUN uv add psycopg2
def connect_db():
    # TODO: Will need config management of course.
    engine = create_engine("postgresql+psycopg2://postgres:mysecretpassword@localhost:5432", echo=True)
    return engine
