from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from models.user import User
from schemas.user import UserCreate
from core.security import get_password_hash, verify_password

class UserService:
    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create_user(db: Session, user: UserCreate):
        try:
            hashed_password = get_password_hash(user.password)
            db_user = User(
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                hashed_password=hashed_password,
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str):
        user = UserService.get_user_by_email(db, email)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user