import bcrypt


def hash_and_salt_password(plain_password: str) -> tuple[str, str]:
    bytes = plain_password.encode("utf-8")
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash.decode("utf-8"), salt.decode("utf-8")


def verify_password(plain_password: str, salt: str, hashed_password: str) -> bool:
    passwd_bytes = plain_password.encode("utf-8")
    salt_bytes = salt.encode("utf-8")
    hash = bcrypt.hashpw(passwd_bytes, salt_bytes).decode("utf-8")
    return hash == hashed_password


# def create_access_token(data: dict, expires_delta: timedelta) -> str:
# from datetime import timedelta
# TODO: Add tests
# password="super-secret-password"

# hash_password(password) == hash_password(password) # False
# verify_password(hash_password(password), password) # True
