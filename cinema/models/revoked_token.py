import datetime

from sqlalchemy import Column, Integer, String, DateTime

from cinema.database.db import base, session


class RevokedTokenModel(base):
    __tablename__ = "revoked_tokens"
    id_ = Column(Integer, primary_key=True)
    jti = Column(String(120))
    blacklisted_on = Column(DateTime, default=datetime.datetime.utcnow)

    def add(self):
        session.add(self)
        session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = session.query(cls).filter_by(jti=jti).first()
        return bool(query)
