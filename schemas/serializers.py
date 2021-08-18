def serialize_dict(data) -> dict:
    try:
        return {**{i:str(data[i]) for i in data if i=='_id'},**{i:data[i] for i in data if i!='_id'}}
    except Exception as e:
        print(e)


def serialize_list(entity) -> list:
    try:
        return [serialize_dict(a) for a in entity]
    except Exception as e:
        print(e)