from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

from api import users_router, files_router, forms_router

from demo_auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(forms_router)
app.include_router(files_router)
app.include_router(users_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
