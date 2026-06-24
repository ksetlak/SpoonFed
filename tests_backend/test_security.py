from automenu_api.security import (
    hash_and_salt_password,
    verify_password,
    create_access_token,
    validate_access_token,
)

password = "super-secret-password"


def test_hash_and_salt_password():
    assert not (hash_and_salt_password(password) == hash_and_salt_password(password))


def test_verify_password():
    hash, salt = hash_and_salt_password(password)
    assert verify_password(hash, salt, password)


user_id = 0


def test_access_token_roundtrip():
    token = create_access_token(0)
    assert validate_access_token(token, 0)
