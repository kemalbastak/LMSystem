from fastapi import FastAPI
from routes.user import user
from routes.library import library


app = FastAPI()
app.include_router(user)
app.include_router(library)
