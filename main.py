from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

from database import Base, engine
from api import users_router, files_router, forms_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(forms_router)
app.include_router(files_router)
app.include_router(users_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
