from pydantic import BaseModel, Field
from typing import Optional
from .user import User

from bson import ObjectId


class Library(BaseModel):
    book_name: str
    author: str
    publisher: str
    category: int
    in_stock:bool = True
    isbn:str
    issued_student:str

