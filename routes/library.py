from helpers.generators import generate_book, generate_isbn
from bson.objectid import ObjectId
from fastapi import APIRouter

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



@library.get('/', tags=["Get Book"]) 
async def find_all_books(limit:int = 10, page:int = 0):
    key = "limit_{}_page_{}".format(str(limit), str(page))
    value = redis_client.get(key)
    if value is None:
        print("not found in cache")
        value = serialize_list(conn.LibMS.library.find())[page : page + limit]
        redis_client.set(key, json.dumps(value))
        return value
    else:
        print("found in cache")
        value = redis_client.get(key)
        return json.loads(value)
    # print(conn.LibMS.library.find())
    # print(serialize_list(conn.LibMS.library.find()))

@library.get('/find_by_book_name/', tags=["Get Book"])
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

@library.post('/library', tags=["Create Book"])
async def create_book(library: Library):
    library.isbn = generate_isbn()
    conn.LibMS.library.insert_one(dict(library))
    print(serialize_list(conn.LibMS.library.find()))
    return serialize_list(conn.LibMS.library.find())

@library.post('/create_many_books', tags=["Create Book"])
async def create_book(amount:int=10):
    books_created = generate_book(amount)
    conn.LibMS.library.insert_many(books_created)
    # print(serialize_list(conn.LibMS.library.find()))
    return serialize_list(books_created)


@library.put('/find_by_id/{id}', tags=["Update Book"])
async def update_book(id, library: Library):
    conn.LibMS.library.find_one_and_update({"_id":ObjectId(id)}, {
        "$set":dict(library)
    })

    return serialize_dict(conn.LibMS.library.find_one({"_id":ObjectId(id)}))

@library.put('/find_by_isbn/{isbn}', tags=["Update Book"])
async def update_book(isbn, library: Library):
    conn.LibMS.library.find_one_and_update({"isbn":isbn}, {
        "$set":dict(library)
    })

    return serialize_dict(conn.LibMS.library.find_one({"isbn":isbn}))



@library.put('/borrow_book/{isbn}', tags=["Update Book"])
async def borrow_book(isbn:str, library: Library):
    # all_users = [i['name'] for i in conn.LibMS.user.find({},{"name"})]
    book_borrow = conn.LibMS.library.find_one({"isbn":isbn})
    filter = {"isbn":isbn}
    if book_borrow["is_given"]:
        return "This book is already given to someone"
    # x = json.loads(book_borrow, object_hook=lambda d: SimpleNamespace(**d))
    # print(x)
    print(library)
    conn.LibMS.library.find_one_and_update(filter, {"$set":{"in_stock": False,"is_given":True}})
    return serialize_dict(conn.LibMS.library.find_one({"isbn":isbn}))


@library.put('/borrow_many_book', tags=["Update Book"])
async def borrow_many_book(amount:int):
    # all_users = [i['name'] for i in conn.LibMS.user.find({},{"name"})]
    book_borrow = conn.LibMS.library.find({"is_given":False})

    for i in range(amount):
        if book_borrow[i]["is_given"]:
            return "This book is already given to someone"
        else:
            conn.LibMS.library.find_one_and_update(book_borrow[i], {"$set":{"in_stock": False,"is_given":True}})
            print(conn.LibMS.library.find_one({"is_given" : True}))
    
    return serialize_list(conn.LibMS.library.find({"is_given" : True}))
           

@library.delete('/delete_by_id/{id}', tags=["Delete Book"])
async def delete_book(id, library: Library):
    return serialize_dict(conn.LibMS.library.find_one_and_delete({"_id":ObjectId(id)}))

@library.delete('/delete_by_isbn/{id}', tags=["Delete Book"])
async def delete_book(isbn, library: Library):
    return serialize_dict(conn.LibMS.library.find_one_and_delete({"isbn":isbn}))

@library.delete('/delete_all_books/', tags=["Delete Book"])
async def delete_book():
    return serialize_dict(conn.LibMS.library.delete_many({}))