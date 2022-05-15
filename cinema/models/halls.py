from sqlalchemy import Column, Integer, String

from cinema.database.db import base, session


class HallModel(base):
    __tablename__ = "halls"
    id = Column(Integer, primary_key=True)
    title = Column(String(30), nullable=False)
    columns = Column(Integer, nullable=False)
    rows = Column(Integer, nullable=False)

    @classmethod
    def find_by_id(cls, id, to_dict=False):
        hall = session.query(cls).filter_by(id=id).first()
        if not hall:
            return {}
        if to_dict:
            return cls.to_dict(hall)
        else:
            return hall

    @classmethod
    def return_all(cls, to_dict=False):
        halls = session.query(cls).order_by(cls.title).all()
        if to_dict:
            return [cls.to_dict(hall) for hall in halls]
        else:
            return list(halls)

    def save_to_db(self):
        session.add(self)
        session.commit()

    @classmethod
    def delete_by_id(cls, id):
        hall = session.query(cls).filter_by(id=id).first()
        if hall:
            hall.is_active = False
            hall.save_to_db()
            return 200
        else:
            return 404

    @staticmethod
    def to_dict(hall):

        return {
            "id": hall.id,
            "title": hall.title,
            "rows": hall.rows,
            "columns": hall.columns,
        }
