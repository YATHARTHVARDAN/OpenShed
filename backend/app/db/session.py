from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os

# Get the URL from Docker Environment Variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the Async Engine
# "echo=True" prints SQL queries to the console (great for debugging)
engine = create_async_engine(DATABASE_URL, echo=True)

# Create the Session Factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

# Dependency Injection for API Routes
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
