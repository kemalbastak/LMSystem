from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import date, datetime

class User(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str
    given_date:Optional[datetime]
    expiration_date:Optional[datetime]


class ShowUser(BaseModel):
    name: str
    surname: str
    email: EmailStr 
    book_id:str = None
    given_date:datetime

    class Config():
        orm_mode = True