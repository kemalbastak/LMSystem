from pydantic import BaseModel

class RequestData(BaseModel):
    amount: int

class Task(BaseModel):
    task_id: str
    status: str

class Result(BaseModel):
    task_id: str
    status: str
