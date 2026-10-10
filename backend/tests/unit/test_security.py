from app.core.security import (
    create_access_token,
    decode_access_token,
    decrypt_secret,
    encrypt_secret,
    hash_password,
    verify_password,
)


def test_password_hashing():
    raw_password = "SuperSecretPassword123!"
    hashed = hash_password(raw_password)
    assert hashed != raw_password
    assert verify_password(raw_password, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False


def test_fernet_secret_encryption():
    secret_api_key = "sk-ant-api03-test-secret-key-for-claude"
    encrypted = encrypt_secret(secret_api_key)
    assert encrypted != secret_api_key
    assert isinstance(encrypted, str)

    decrypted = decrypt_secret(encrypted)
    assert decrypted == secret_api_key


def test_jwt_token_generation_and_decoding():
    user_id = "user_123456"
    role = "admin"
    token = create_access_token(subject=user_id, role=role, token_version=2)
    assert isinstance(token, str)

    payload = decode_access_token(token)
    assert payload["sub"] == user_id
    assert payload["role"] == role
    assert payload["ver"] == 2
    assert "jti" in payload
    assert "exp" in payload
