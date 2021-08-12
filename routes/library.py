from bson.objectid import ObjectId
from fastapi import APIRouter

from models.user import User
from models.library import Library

from config.db import conn
from schemas.user import serialize_dict, serialize_list

from bson import ObjectId


library = APIRouter()

@library.get('/api/v1/library', tags=["Library"])
async def find_all_books():
    print(conn.local.library.find())
    print(serialize_list(conn.local.library.find()))
    return serialize_list(conn.local.library.find())

@library.get('/api/v1/library/{id}', tags=["Library"])
async def find_one_book(id):
    return serialize_dict(conn.local.library.find_one({"_id":ObjectId(id)}))

@library.post('/api/v1/library', tags=["Library"])
async def create_book(library: Library):
    conn.local.library.insert_one(dict(library))
    print(serialize_list(conn.local.library.find()))
    return serialize_list(conn.local.library.find())

@library.put('/api/v1/library/{id}', tags=["Library"])
async def update_book(id, library: Library):
    conn.local.library.find_one_and_update({"_id":ObjectId(id)}, {
        "$set":dict(library)
    })

    return serialize_dict(conn.local.library.find_one({"_id":ObjectId(id)}))


@library.delete('/api/v1/library/{id}', tags=["Library"])
async def delete_book(id, library: Library):
    return serialize_dict(conn.local.library.find_one_and_delete({"_id":ObjectId(id)}))