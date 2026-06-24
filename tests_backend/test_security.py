from automenu_api.security import hash_and_salt_password, verify_password

password = "super-secret-password"


def test_hash_and_salt_password():
    assert not (hash_and_salt_password(password) == hash_and_salt_password(password))


def test_verify_password():
    hash, salt = hash_and_salt_password(password)
    assert verify_password(hash, salt, password)


# TODO
# def test_create_access_token():
