import datetime
import json

from sqlalchemy import Column, Integer, Date, Time, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from cinema.database.db import base, session as db_session
from .halls import HallModel
from .movies import MovieModel


class SessionModel(base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    movie = relationship(MovieModel)
    date = Column(Date)
    start_at = Column(Time())
    end_at = Column(Time())
    hall_id = Column(Integer, ForeignKey("halls.id"), nullable=False)
    hall = relationship(HallModel)
    is_active = Column(Boolean, default=True)
    tickets_price = Column(Integer, nullable=False, default=0)

    def save_to_db(self):
        db_session.add(self)
        db_session.commit()

    @classmethod
    def find_by_id(cls, id: int, to_dict: bool = False):
        session = db_session.query(cls).filter_by(id=id).first()
        if not session:
            return {}
        if to_dict:
            return cls.to_dict(session)
        else:
            return session

    @classmethod
    def find_by_movie_id(cls, movie_id: int, to_dict: bool = False):
        sessions = (
            db_session.query(cls).filter_by(movie_id=movie_id).order_by(cls.date).all()
        )
        if not sessions:
            return {}
        if to_dict:
            return [cls.to_dict(session) for session in sessions]
        else:
            return sessions

    @classmethod
    def for_search(
            cls,
            movie_id: int = 0,
            date: datetime.date = datetime.date(day=1, month=1, year=2000),
            genres: str = "",
            actors: str = "",
            producer: str = "",
            to_dict: bool = False,
        ):
        print(producer , actors , genres)
        if movie_id:
            if date != datetime.date(day=1, month=1, year=2000):
                sessions = (
                    db_session.query(cls)
                        .filter_by(movie_id=movie_id, date=date)
                        .order_by(cls.date)
                        .all()
                )
            else:
                sessions = (
                    db_session.query(cls)
                        .filter_by(movie_id=movie_id)
                        .order_by(cls.date)
                        .all()
                )
        else:
            if date != datetime.date(day=1, month=1, year=2000):
                sessions = (
                    db_session.query(cls).filter_by(date=date).order_by(cls.date).all()
                )
            else:
                sessions = db_session.query(cls).order_by(cls.date).all()

        if genres:
            print(1)
            for session in sessions:
                if not genres in session.movie.genres:
                    sessions.remove(session)
        if actors:
            for session in sessions:
                if not actors in session.movie.actors:
                    sessions.remove(session)
        if producer:
            for session in sessions:
                if not producer in session.movie.producer:
                    sessions.remove(session)
        if not sessions:
            return {}
        if to_dict:
            return [cls.to_dict(session) for session in sessions]
        else:
            print(len(sessions))
            return sessions

    @classmethod
    def return_all(cls, to_dict=False):
        sessions = (
            db_session.query(cls).filter_by(is_active=True).order_by(cls.date).all()
        )
        if to_dict:
            return [cls.to_dict(session) for session in sessions]
        else:
            return list(sessions)

    @classmethod
    def delete_by_id(cls, id):
        session = db_session.query(cls).filter_by(id=id).first()
        if session:
            session.is_active = False
            session.save_to_db()
            return 200
        else:
            return 404

    @staticmethod
    def to_dict(session):
        if session.is_active:
            return {
                "id": session.id,
                "movie_id": session.movie_id,
                "hall_id": session.hall_id,
                "date": json.dumps(session.date, default=str).strip('"'),
                "start_at": json.dumps(session.start_at, default=str).strip('"'),
                "end_at": json.dumps(session.end_at, default=str).strip('"'),
                "tickets_price": session.tickets_price,
            }
        else:
            return {"message": "Session was deleted"}
