import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from cryptography.fernet import Fernet, InvalidToken

from app.core.config import get_settings

settings = get_settings()
_pwd_hasher = PasswordHasher()


# --- Password Hashing (Argon2) ---


def hash_password(password: str) -> str:
    """Hash password using Argon2id algorithm."""
    return _pwd_hasher.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hashed string."""
    try:
        return _pwd_hasher.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False
    except Exception:
        return False


# --- Encryption at rest (Fernet) ---


def get_fernet() -> Fernet:
    """Obtain configured Fernet instance."""
    raw_key = settings.ENCRYPTION_KEY
    key_bytes: bytes = raw_key.encode("utf-8") if isinstance(raw_key, str) else raw_key
    return Fernet(key_bytes)


def encrypt_secret(plain_text: str) -> str:
    """Encrypt a secret string (e.g. LLM API Key) using Fernet symmetric encryption."""
    if not plain_text:
        return ""
    fernet = get_fernet()
    encrypted_bytes = fernet.encrypt(plain_text.encode("utf-8"))
    return encrypted_bytes.decode("utf-8")


def decrypt_secret(cipher_text: str) -> str:
    """Decrypt a Fernet cipher text back to plain text."""
    if not cipher_text:
        return ""
    fernet = get_fernet()
    try:
        decrypted_bytes = fernet.decrypt(cipher_text.encode("utf-8"))
        return decrypted_bytes.decode("utf-8")
    except InvalidToken:
        raise ValueError("Invalid encryption token or key mismatch.") from None


# --- JWT Helpers ---


def create_access_token(
    subject: str,
    role: str = "employee",
    token_version: int = 1,
    expires_delta: timedelta | None = None,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    """Create JWT access token with 30-day default expiry and jti."""
    now = datetime.now(UTC)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)

    payload: dict[str, Any] = {
        "sub": subject,
        "role": role,
        "ver": token_version,
        "jti": str(uuid.uuid4()),
        "iat": now,
        "exp": expire,
    }
    if extra_claims:
        payload.update(extra_claims)

    encoded_jwt = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode and validate JWT access token."""
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )
