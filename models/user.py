from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class User(BaseModel):
    name: str
    email: EmailStr
    password: str
    book_id:str = None
    given_date:datetime


# class ShowUser(BaseModel):
#     name: str
#     email: EmailStr 
#     book_id:str
#     given_date:datetime

#     class Config():
#         orm_mode = True