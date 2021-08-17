from helpers.generators import generate_book_id
from bson.objectid import ObjectId
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
 


from models.user import User
from models.library import Library

from config.db import conn
from config.redis_cli import redis_client
from schemas.serializers import serialize_dict, serialize_list

from bson import ObjectId

import json



library = APIRouter()

@library.get("/")
async def redirect_docs():
    return RedirectResponse("/docs")

@library.get('/api/v1/library', tags=["Library"]) 
async def find_all_books():
    aa = redis_client.get('f')
    print(conn.LibMS.library.find())
    print(serialize_list(conn.LibMS.library.find()))
    return serialize_list(conn.LibMS.library.find())

@library.get('/api/v1/library/{book_name}', tags=["Library"])
async def find_one_book(book_name):
    book_key = f"{book_name}_key"
    # redis_client.get()
    return serialize_dict(conn.LibMS.library.find_one({"book_ame":book_name}))

@library.post('/api/v1/library', tags=["Library"])
async def create_book(library: Library):
    #library.isbn = generate_book_id(conn)
    conn.LibMS.library.insert_one(dict(library))
    print(serialize_list(conn.LibMS.library.find()))
    return serialize_list(conn.LibMS.library.find())




@library.put('/api/v1/library/{id}', tags=["Library"])
async def update_book(id, library: Library):
    conn.LibMS.library.find_one_and_update({"_id":ObjectId(id)}, {
        "$set":dict(library)
    })

    return serialize_dict(conn.LibMS.library.find_one({"_id":ObjectId(id)}))


@library.delete('/api/v1/library/{id}', tags=["Library"])
async def delete_book(id, library: Library):
    return serialize_dict(conn.LibMS.library.find_one_and_delete({"_id":ObjectId(id)}))