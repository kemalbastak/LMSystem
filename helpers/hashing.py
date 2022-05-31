from passlib.context import CryptContext


pwd = CryptContext(schemes=["bcrypt"], deprecated = "auto")

class Hash:
    def bcrypt(password):
        hashed_pwd = pwd.hash(password)
        return hashed_pwd

def test():
    pass