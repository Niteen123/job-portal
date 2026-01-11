import hashlib


def hash_password(password: str) -> str:
    """Hash a plain text password using SHA-256 (suitable for a demo/resume project).

    Note: For production use a slow password hash (bcrypt/argon2). Kept simple here
    to avoid environment-specific native dependency issues in the container.
    """
    if not isinstance(password, (str, bytes)):
        password = str(password)
    if isinstance(password, str):
        password = password.encode("utf-8")
    return hashlib.sha256(password).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    if isinstance(plain_password, str):
        plain_password = plain_password.encode("utf-8")
    return hashlib.sha256(plain_password).hexdigest() == hashed_password
