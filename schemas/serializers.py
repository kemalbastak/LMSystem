def serialize_dict(data) -> dict:
    return {**{i:str(data[i]) for i in data if i=='_id'},**{i:data[i] for i in data if i!='_id'}}

def serialize_list(entity) -> list:
    return [serialize_dict(a) for a in entity]