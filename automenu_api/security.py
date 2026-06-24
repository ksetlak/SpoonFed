from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from config import settings

JWT_VALIDITY = timedelta(hours=settings.jwt_validity)


def hash_and_salt_password(plain_password: str) -> tuple[str, str]:
    bytes = plain_password.encode("utf-8")
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash.decode("utf-8"), salt.decode("utf-8")


def verify_password(hashed_password: str, salt: str, plain_password: str) -> bool:
    passwd_bytes = plain_password.encode("utf-8")
    salt_bytes = salt.encode("utf-8")
    hash = bcrypt.hashpw(passwd_bytes, salt_bytes).decode("utf-8")
    return hash == hashed_password


def create_access_token(sub: int, expires_delta: timedelta = JWT_VALIDITY) -> str:
    expire = datetime.now(timezone.utc) + expires_delta

    data = {
        "sub": str(sub),  # str() cast because it's supposedly a OAuth2 standard practice.
        "exp": expire,
        "iat": int(datetime.now(timezone.utc).timestamp()),
    }

    encoded_jwt = jwt.encode(data, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

    return encoded_jwt
