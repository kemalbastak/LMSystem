from bson.objectid import ObjectId
from fastapi import APIRouter

from models.user import User
from config.db import conn
from schemas.user import serialize_dict, serialize_list

from bson import ObjectId
user = APIRouter()


@user.get('/api/v1/user')
async def find_all_users():
    print(conn.local.user.find())
    print(serialize_list(conn.local.user.find()))
    return serialize_list(conn.local.user.find())

@user.get('/api/v1/user/{id}')
async def find_one_user(id):
    return serialize_dict(conn.local.user.find_one({"_id":ObjectId(id)}))

@user.post('/api/v1/user')
async def create_user(user: User):
    conn.local.user.insert_one(dict(user))
    return serialize_list(conn.local.user.find())

@user.put('/api/v1/user/{id}')
async def create_user(id, user: User):
    conn.local.user.find_one_and_update({"_id":ObjectId(id)}, {
        "$set":dict(user)
    })

    return serialize_dict(conn.local.user.find_one({"_id":ObjectId(id)}))


@user.delete('/api/v1/user/{id}')
async def delete_user(id, user: User):
    return serialize_dict(conn.local.user.find_one_and_delete({"_id":ObjectId(id)}))