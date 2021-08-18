from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes.user import user
from routes.library import library


app = FastAPI()
app.include_router(user)
app.include_router(library)

