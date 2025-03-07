from sqlalchemy.orm import Session
from config.db_config import engine
from models.user_table import Users


class DBHelper:
    def get_user_by_username(username: str):
        with Session(engine) as session:
            return session.query(Users).filter(Users.username == username).first()

    def get_user_by_id(user_id: int):
        with Session(engine) as session:
            return session.query(Users).filter(Users.id == user_id).first()
