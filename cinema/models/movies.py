from sqlalchemy import Column, Integer, String, Text, Boolean

from cinema.database.db import base, session


class MovieModel(base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(Text(), nullable=False)
    year = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    genres = Column(String(100), nullable=False)
    actors = Column(String(500), nullable=False)
    producer = Column(String(100), nullable=False)
    age_rating = Column(String(5), nullable=False)
    in_rental = Column(Boolean, default=True)

    @classmethod
    def find_by_id(cls, id, to_dict=False):
        movie = session.query(cls).filter_by(id=id).first()
        if not movie:
            return {}
        if to_dict:
            return cls.to_dict(movie)
        else:
            return movie

    @classmethod
    def find_by_title(cls, title, to_dict=False):
        movie = session.query(cls).filter_by(title=title).first()
        if not movie:
            return {}
        if to_dict:
            return cls.to_dict(movie)
        else:
            return movie

    @classmethod
    def return_all(cls, to_dict=False):
        movies = session.query(cls).order_by(cls.title).all()
        if to_dict:
            return [cls.to_dict(movie) for movie in movies]
        else:
            return list(movies)

    @classmethod
    def return_all_in_rental(cls, to_dict=False):
        movies = session.query(cls).filter_by(in_rental=True).order_by(cls.title).all()
        if to_dict:
            return [cls.to_dict(movie) for movie in movies]
        else:
            return list(movies)

    def save_to_db(self):
        session.add(self)
        session.commit()

    @classmethod
    def delete_by_id(cls, id):
        movie = session.query(cls).filter_by(id=id).first()
        if movie:
            movie.in_rental = False
            movie.save_to_db()
            return 200
        else:
            return 404

    @staticmethod
    def to_dict(movie):
        if movie.in_rental:
            return {
                "id": movie.id,
                "title": movie.title,
                "description": movie.description,
                "duration": movie.duration,
                "year": movie.year,
                "actors": movie.actors,
                "producer": movie.producer,
                "genres": movie.genres,
                "age_rating": movie.age_rating,
            }
        else:
            return {"message": "Movie not in rental"}
