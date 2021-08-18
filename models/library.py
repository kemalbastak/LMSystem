from pydantic import BaseModel, Field
from typing import Optional
from .user import User
from datetime import datetime

from bson import ObjectId


class Library(BaseModel):
    book_name: str
    author: str
    publisher: str
    in_stock:bool = True
    isbn:str
    issued_student:str
    is_given:bool

