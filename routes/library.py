from helpers.generators import generate_book, generate_isbn
from bson.objectid import ObjectId
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
 
from types import SimpleNamespace

from models.user import User
from models.library import Library

from config.db import conn
from config.redis_cli import redis_client
from schemas.serializers import serialize_dict, serialize_list

from bson import ObjectId

import json, random, re



library = APIRouter()

def regx(param):
    return re.compile(param, re.IGNORECASE)



@library.get("/")
async def redirect_docs():
    return RedirectResponse("/docs")

@library.get('/api/v1/library', tags=["Get Book"]) 
async def find_all_books(limit:int = 10, page:int = 0):
    aa = redis_client.get('f')
    # print(conn.LibMS.library.find())
    # print(serialize_list(conn.LibMS.library.find()))
    return serialize_list(conn.LibMS.library.find())[page : page + limit]

@library.get('/api/v1/library/find_by_book_name/', tags=["Get Book"])
async def find_one_book(book_name):
    book_key = "{}_key".format(book_name.replace(" ",""))
    value = redis_client.get(book_key)
    print(value)
    if value is None:
        print(conn.LibMS.library.find_one({"book_name" : {"$regex" : regx(book_name)}}))
        value = serialize_dict(conn.LibMS.library.find_one({"book_name" : {"$regex" : regx(book_name)}}))
        redis_client.set(book_key, json.dumps(value))
        print("not found in cache")
        return value
    else:
        print("found in cache")
        value = redis_client.get(book_key)
        return json.loads(value)

    # redis_client.get()

@library.post('/api/v1/library', tags=["Create Book"])
async def create_book(library: Library):
    library.isbn = generate_isbn()
    conn.LibMS.library.insert_one(dict(library))
    print(serialize_list(conn.LibMS.library.find()))
    return serialize_list(conn.LibMS.library.find())

@library.post('/api/v1/library/create_many_books', tags=["Create Book"])
async def create_book(amount:int=10):
    books_created = generate_book(amount)
    conn.LibMS.library.insert_many(books_created)
    # print(serialize_list(conn.LibMS.library.find()))
    return serialize_list(books_created)


@library.put('/api/v1/library/find_by_id/{id}', tags=["Update Book"])
async def update_book(id, library: Library):
    conn.LibMS.library.find_one_and_update({"_id":ObjectId(id)}, {
        "$set":dict(library)
    })

    return serialize_dict(conn.LibMS.library.find_one({"_id":ObjectId(id)}))

@library.put('/api/v1/library/find_by_isbn/{isbn}', tags=["Update Book"])
async def update_book(isbn, library: Library):
    conn.LibMS.library.find_one_and_update({"isbn":isbn}, {
        "$set":dict(library)
    })

    return serialize_dict(conn.LibMS.library.find_one({"isbn":isbn}))



@library.put('/api/v1/user/borrow_book/{isbn}', tags=["Update Book"])
async def borrow_book(isbn:str, library: Library):
    all_users = [i['name'] for i in conn.LibMS.user.find({},{"name"})]
    book_borrow = conn.LibMS.library.find_one({"isbn":isbn})
    if book_borrow["is_given"]:
        return "This book is already given to someone"
    # x = json.loads(book_borrow, object_hook=lambda d: SimpleNamespace(**d))
    # print(x)
    print(library)
    book_borrow.update_one({"$set":{"in_stock": False,"is_given":True, "issued_student": random.choice(all_users)}})
    return serialize_dict(conn.LibMS.library.find_one({"isbn":isbn}))

@library.delete('/api/v1/library/delete_by_id/{id}', tags=["Delete Book"])
async def delete_book(id, library: Library):
    return serialize_dict(conn.LibMS.library.find_one_and_delete({"_id":ObjectId(id)}))

@library.delete('/api/v1/library/delete_by_isbn/{id}', tags=["Delete Book"])
async def delete_book(isbn, library: Library):
    return serialize_dict(conn.LibMS.library.find_one_and_delete({"isbn":isbn}))

@library.delete('/api/v1/library/delete_all_books/', tags=["Delete Book"])
async def delete_book():
    return serialize_dict(conn.LibMS.library.delete_many({}))