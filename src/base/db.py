import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from .config import settings

DATABASE_CONNECTION_STRING = (
    settings.connection_string.replace(
        os.getenv("DB_NAME"), f"test_{os.getenv('DB_NAME')}"
    )
    if "PYTEST_VERSION" in os.environ
    else settings.connection_string
)
async_engine = create_async_engine(DATABASE_CONNECTION_STRING, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncSession:  # type: ignore
    async with AsyncSessionLocal() as session:
        yield session


Base = declarative_base()
