from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy import text
from app.db.session import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 OpenShed System Starting...")
    
    # 1. Test the Real Database Connection
    try:
        async with engine.begin() as conn:
            # Run a simple SQL query
            await conn.execute(text("SELECT 1"))
        print("✅ Database Connection: ACTIVE (Asyncpg)")
    except Exception as e:
        print(f"❌ Database Connection: FAILED - {e}")
        
    yield
    
    # 2. Close connection on shutdown
    await engine.dispose()
    print("🛑 OpenShed System Shutting Down...")

app = FastAPI(
    title="OpenShed API",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {"message": "Welcome to OpenShed API", "status": "operational"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
