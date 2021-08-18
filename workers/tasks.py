from .celery_worker import celery
from celery.utils.log import get_task_logger
from routes.library import borrow_many_book

celery_log = get_task_logger(__name__)

@celery.task(name='routes.library.borrow_many_book')
def book_task(amount):
    borrow_many_book(amount)
    celery_log.info(f"Celery task completed!")
    return 'OK'