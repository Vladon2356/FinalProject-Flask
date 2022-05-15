from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy import Column, Integer, String, Boolean

from cinema.database.db import base, session


class UserModel(base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String(50))
    hashed_password = Column(String(100), nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    @classmethod
    def find_by_id(cls, id, to_dict=False):
        user = session.query(cls).filter_by(id=id, is_active=True).first()
        if not user:
            return {}
        if to_dict:
            return cls.to_dict(user)
        else:
            return user

    @classmethod
    def find_by_first_and_last_name(cls, first_name, last_name, to_dict=False):
        user = (
            session.query(cls)
            .filter_by(first_name=first_name, last_name=last_name, is_active=True)
            .first()
        )
        if not user:
            return {}
        if to_dict:
            return cls.to_dict(user)
        else:
            return user

    @classmethod
    def find_by_email(cls, email, to_dict=False):
        user = session.query(cls).filter_by(email=email, is_active=True).first()
        if not user:
            return {}
        if to_dict:
            return cls.to_dict(user)
        else:
            return user

    @classmethod
    def return_all(cls, to_dict=False):
        users = session.query(cls).order_by(cls.id).all()
        if to_dict:
            return [cls.to_dict(user) for user in users]
        else:
            return list(users)

    @classmethod
    def return_all_is_active(cls, to_dict=False):
        users = session.query(cls).filter_by(is_active=True).order_by(cls.id).all()
        if to_dict:
            return [cls.to_dict(user) for user in users]
        else:
            return list(users)

    def save_to_db(self):
        session.add(self)
        session.commit()

    @classmethod
    def delete_by_id(cls, id):
        user = session.query(cls).filter_by(id=id).first()
        if user:
            user.is_active = False
            user.save_to_db()
            return 200
        else:
            return 404

    @staticmethod
    def to_dict(user):
        if user.is_active:
            return {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "age": user.age,
                "email": user.email,
                "is_admin": user.is_admin,
                "is_active": user.is_active,
            }
        else:
            return {"message": "User was deleted"}

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)
