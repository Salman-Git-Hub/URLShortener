import secrets
import string
from sqlalchemy.orm import Session
from . import crud


def generate_key(size: int = 5) -> str:
    key = "".join(secrets.choice(string.ascii_letters) for _ in range(size))
    return key


def create_unique_key(db: Session) -> str:
    key = generate_key()
    while crud.get_url_by_key(db, key):
        key = generate_key()
    return key
