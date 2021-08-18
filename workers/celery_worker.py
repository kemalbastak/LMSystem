from celery import Celery

CELERY_BROKER_URL = "redis://localhost:6379" # os.getenv("REDISSERVER", "redis://redis_server:6379")
CELERY_RESULT_BACKEND = "redis://localhost:6379" # os.getenv("REDISSERVER", "redis://redis_server:6379")
print(CELERY_BROKER_URL)
INCLUDE = ["workers.tasks"]

celery = Celery("celery", backend=CELERY_RESULT_BACKEND, broker=CELERY_BROKER_URL, include=INCLUDE)