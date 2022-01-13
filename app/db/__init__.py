from sqlalchemy.ext.asyncio import create_async_engine, async_scoped_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


from sqlalchemy.ext.declarative import declarative_base


import asyncio

from os import getenv

from sqlalchemy import MetaData


# Comment when using alembic

database_url = getenv("DATABASE_URL")
engine = create_async_engine(database_url, echo=True)
db_session = async_scoped_session(
    sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, future=True),
    scopefunc=asyncio.current_task,
)

# ---------------------------

meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
)

Base = declarative_base(metadata=meta)


def init_db():
    import core.entities
