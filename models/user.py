from typing import Optional
from pydantic import BaseModel
from datetime import datetime
class User(BaseModel):
    name: str
    email: str
    password: str
    book_id:str = None
    given_date:datetime