import random
from config.db import conn
from faker import Faker
from bson import ObjectId
from datetime import datetime, timedelta
from helpers.hashing import Hash 

fake = Faker()

def generate_isbn():
	isbn_num = str(random.randrange(1000000000,9999999999))
	return f"{isbn_num[0:1]}-{isbn_num[1:4]}-{isbn_num[4:7]}-{isbn_num[7:8]}"

def generate_book(amount:int):
	book_list = []
	
	for _ in range(amount):
		isbn = generate_isbn()
		book = {
			"_id": ObjectId(),
			"book_name": fake.name(),
			"author":fake.name(),
			"publisher":fake.bs().title(),
			"in_stock": True,
			"isbn": isbn,
			"issued_student": "",
			"is_given":False

		}
		book_list.append(book)
	#print(book_list)
	return book_list 

def generate_user(amount:int):
	user_list = []
	for _ in range(amount):
		
		user = {
			"_id": ObjectId(),
			"name":fake.first_name(),
			"surname": fake.last_name(),
			"password": Hash.bcrypt(fake.password()),
			"given_date": "",
			"expiration_date": "",
		}
		user_list.append(user)

	return user_list


# conn.LibMS.library.insert_many(generate_book(1000))




