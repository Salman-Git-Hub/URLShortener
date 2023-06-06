from sqlalchemy.orm import Session
from . import keygen, models, schemas


def create_url(db: Session, url: schemas.URLBase) -> models.URL:
    key = keygen.create_unique_key(db)
    admin_key = f"{key}_{keygen.generate_key(10)}"
    db_url = models.URL(
        target_url=url.target_url,
        key=key,
        admin_key=admin_key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def get_all_url(db: Session):
    return db.query(models.URL).all()


def get_url_by_key(db: Session, url_key: str) -> models.URL:
    return (
        db.query(models.URL)
        .filter(models.URL.key == url_key, models.URL.is_active)
        .first()
    )


def get_url_by_admin_key(db: Session, admin_key: str) -> models.URL:
    return (
        db.query(models.URL)
        .filter(models.URL.admin_key == admin_key, models.URL.is_active)
        .first()
    )


def get_not_active_url(db: Session, admin_key: str) -> models.URL:
    return (
        db.query(models.URL)
        .filter(models.URL.admin_key == admin_key)
        .first()
    )


def update_view_count(db: Session, db_url: models.URL) -> models.URL:
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url


def update_url(db: Session, db_url: models.URL):
    db_url.is_active = not db_url.is_active
    db.commit()
    db.refresh(db_url)
    return
