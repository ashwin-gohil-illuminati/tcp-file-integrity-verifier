from fastapi import FastAPI
from .routers import user, auth, hash

from . import models
from .database import engine, SessionLocal, get_db




models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(user.router)
app.include_router(auth.router)
app.include_router(hash.router)


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI!!!!"}