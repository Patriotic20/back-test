import os

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.base.config import settings
from src.base.db import Base

DATABASE_CONNECTION_STRING = settings.connection_string.replace(
    os.getenv("DB_NAME"), f"test_{os.getenv('DB_NAME')}"
)

test_async_engine = create_async_engine(DATABASE_CONNECTION_STRING, echo=False)

TestAsyncSessionLocal = sessionmaker(
    bind=test_async_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(autouse=True)
async def db():
    async with TestAsyncSessionLocal() as session:
        async with test_async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

        yield session

    await session.close()
