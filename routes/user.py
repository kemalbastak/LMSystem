from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException


from models.user import User, ShowUser
from config.db import conn
from schemas.serializers import serialize_dict, serialize_list
from helpers.hashing import Hash 

from bson import ObjectId

import re


user = APIRouter()



@user.get('/api/v1/user', tags=["Get User"], response_model_exclude={"password"}) #, response_model=ShowUser
async def find_all_users():
    print(conn.local.user.find())
    print(serialize_list(conn.LibMS.user.find()))
    return serialize_list(conn.LibMS.user.find())

@user.get('/api/v1/user/{id}', tags=["Get User"])
async def find_one_user(id):
    user = conn.LibMS.user.find_one({"_id":ObjectId(id)})
    if not user:
        raise HTTPException(status_code=404, detail=f"Student with Id: {id} not found!")
    user = serialize_dict(user)
    return user

#Finds by name
@user.get('/api/v1/user/', tags=["Get User"])
async def find_by_name(name):
    regx = re.compile(name, re.IGNORECASE)
    user = conn.LibMS.user.find_one({"name" : {"$regex" : regx}})
    print(user)
    if not user:
        raise HTTPException(status_code=404, detail=f"Student with Id: {name} not found!")
    user = serialize_dict(user)
    return user

@user.post('/api/v1/user', tags=["Post User"])
async def create_user(user: User):
    user.password = Hash.bcrypt(user.password)
    conn.LibMS.user.insert_one(dict(user))
    return serialize_list(conn.LibMS.user.find())

@user.put('/api/v1/user/{id}', tags=["Update User"])
async def update_user(id, user: User):
    conn.LibMS.user.find_one_and_update({"_id":ObjectId(id)}, {
        "$set":dict(user)
    })

    return serialize_dict(conn.local.user.find_one({"_id":ObjectId(id)}))


@user.delete('/api/v1/user/{id}', tags=["Delete User"])
async def delete_user(id, user: User):
    return serialize_dict(conn.local.user.find_one_and_delete({"_id":ObjectId(id)}))