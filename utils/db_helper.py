from models.user_table import Users
from config.db_config import SessionLocal


class DBHelper:
    def get_user_by_email(email: str):
        with SessionLocal() as session:
            return session.query(Users).filter(Users.email == email).first()

    def get_user_by_username(username: str):
        with SessionLocal() as session:
            return session.query(Users).filter(Users.username == username).first()

    def get_user_by_id(user_id: int):
        with SessionLocal() as session:
            return session.query(Users).filter(Users.id == user_id).first()
