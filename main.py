from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from car_service.models import db_helper
from car_service.config import settings
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    #startup
    with db_helper.engine.connect() as conn:
        print(conn.execute(text("SELECT 1")).fetchall())
    yield
    #shutdown
    db_helper.dispose()


app = FastAPI(lifespan=lifespan)

@app.get('/health')
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )