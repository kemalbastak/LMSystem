from pydantic import BaseModel, Field
from typing import Optional
from .user import User

from bson import ObjectId

class UserObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')

class Library(BaseModel):
    book_name: str
    author: str
    publisher: str
    category: int
    in_stock:bool = True
    isbn:str
    given_who:str

    