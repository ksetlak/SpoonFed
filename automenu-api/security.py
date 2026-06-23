import bcrypt


def hash_password(plain_password: str) -> str:
    bytes = plain_password.encode("utf-8")
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    hash = hash.decode("utf-8")
    return hash


def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    return hash_password(plain_password) == hashed_password
