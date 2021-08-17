def generate_book_id(collection):
	for x in range(200000,500000):
		if collection.find_one({"_id":x}) is None:
			return x

			