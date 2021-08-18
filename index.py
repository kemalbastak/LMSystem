from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes.user import user
from routes.library import library
from routes.celery_viewer import celery



app = FastAPI()
app.include_router(user, prefix='/api/v1/user')
app.include_router(library, prefix='/api/v1/library')
app.include_router(celery, prefix='/api/v1/celery')

