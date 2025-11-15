# python
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import init_db
# example router registration
from app.routers import auth, tasks

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: initialize DB (or run other startup tasks)
    init_db()
    yield
    # shutdown: add cleanup here if needed

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(tasks.router)

