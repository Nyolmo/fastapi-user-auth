from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.db_base import Base

#Base = declarative_base()



engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, autocommit=False, autoflush=False)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session