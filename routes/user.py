from helpers.generators import generate_user
from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException


from models.user import User, ShowUser
from config.db import conn
from schemas.serializers import serialize_dict, serialize_list
from helpers.hashing import Hash 

from bson import ObjectId

import re


user = APIRouter()

def regx(param):
    return re.compile(param, re.IGNORECASE)

@user.get('/api/v1/user', tags=["Get User"], response_model_exclude={"password"}) #, response_model=ShowUser
async def find_all_users(limit:int = 10, page:int = 0):
    print(conn.local.user.find())
    print(serialize_list(conn.LibMS.user.find()))
    return serialize_list(conn.LibMS.user.find())[page : page + limit]


#Finds by name
@user.get('/api/v1/user/{name}', tags=["Get User"])
async def find_by_name(name):
    user = conn.LibMS.user.find_one({"name" : {"$regex" : regx(name)}})
    print(user)
    if not user:
        raise HTTPException(status_code=404, detail=f"Student with Name: {name} not found!")
    user = serialize_dict(user)
    return user

@user.post('/api/v1/user', tags=["Post User"])
async def create_user(user: User):
    user.password = Hash.bcrypt(user.password)
    conn.LibMS.user.insert_one(dict(user))
    return serialize_list(conn.LibMS.user.find())

@user.post('/api/v1/user/create_many_users', tags=["Post User"])
async def create_user(amount:int=10):
    users_created = generate_user(amount)
    print(users_created)
    conn.LibMS.user.insert_many(users_created)
    # print(serialize_list(conn.LibMS.library.find()))
    return serialize_list(users_created)

@user.put('/api/v1/user/{id}', tags=["Update User"])
async def update_user(id, user: User):
    conn.LibMS.user.find_one_and_update({"_id":ObjectId(id)}, {
        "$set":dict(user)
    })

    return serialize_dict(conn.local.user.find_one({"_id":ObjectId(id)}))




@user.delete('/api/v1/user/{id}', tags=["Delete User"])
async def delete_user(id, user: User):
    return serialize_dict(conn.local.user.find_one_and_delete({"_id":ObjectId(id)}))