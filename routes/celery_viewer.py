from celery.result import AsyncResult
from celery import current_task
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.celery_model import Task, Result, RequestData
from workers.tasks import book_task, borrow_many_book




celery = APIRouter()

@celery.post('/request_status', response_model=Task, status_code=202, tags=["Celery Task"])
async def run_borrow_book(request_data:RequestData):
    task_id = book_task.delay(request_data.amount)
    print(task_id)
    return {'task_id': str(task_id), 'status': 'Processing'}

@celery.get('/get_task_status',response_model=Result, status_code=200,
            responses={202: {'model': Task, 'description': 'Accepted: Not Ready'}}, tags=["Celery Task"])
async def get_task_status(task_id):
    task = AsyncResult(task_id)
    print(task.status)
    if not task.ready():
        return JSONResponse(status_code=202, content={'task_id': str(task_id), 'status': 'Processing'})
    result = task.get()
    return {'task_id': task_id, 'status': str(result)}