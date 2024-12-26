import pytest
from sqlalchemy.ext.asyncio import AsyncSession , create_async_engine
from sqlalchemy.orm import sessionmaker
from src.settings.config import settings
from src.settings.db import Base


DATABASE_CONNECTION_STRING = settings.connection_string

test_async_engine = create_async_engine(DATABASE_CONNECTION_STRING , echo= True)

TestAsyncSessionLocal = sessionmaker(
    bind=test_async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

@pytest.fixture
async def db():
    async with TestAsyncSessionLocal() as session:
        # async with test_async_engine.begin() as conn:
        #     await conn.run_sync(Base.metadata.drop_all)
        #     await conn.run_sync(Base.metadata.create_all)
            
        yield session
        
    await session.close()