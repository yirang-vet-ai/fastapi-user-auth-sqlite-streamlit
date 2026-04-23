from sqlalchemy import or_
from sqlalchemy.orm import Session

from app import models
from app.auth import hash_password, verify_password


def get_user_by_username(db: Session, username: str):
    return db.query(models.Member).filter(models.Member.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.Member).filter(models.Member.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.Member).filter(models.Member.id == user_id).first()


def get_all_users(db: Session):
    return db.query(models.Member).order_by(models.Member.id.asc()).all()


def create_user(db: Session, username: str, email: str, nickname: str | None, password: str):
    db_user = models.Member(
        username=username,
        email=email,
        nickname=nickname,
        hashed_password=hash_password(password),
        is_active=True,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username_or_email: str, password: str):
    user = (
        db.query(models.Member)
        .filter(
            or_(
                models.Member.username == username_or_email,
                models.Member.email == username_or_email
            )
        )
        .first()
    )

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


def change_password(db: Session, user_id: int, new_password: str):
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    user.hashed_password = hash_password(new_password)
    db.commit()
    db.refresh(user)
    return user