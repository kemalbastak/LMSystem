This project is a Library Management System built with FastAPI

To install venv run

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

To run the application you first need to go to the directory file and run

docker-compose up

Then open another command prompt and run

uvicorn index:app --reload

To run celery open another command prompt and run 

celery -A workers.celery_worker worker --loglevel=INFO

