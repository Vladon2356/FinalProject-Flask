from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from cinema.database.db import base, session as db_session
from .session import SessionModel
from .users import UserModel


class TicketModel(base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True)
    price = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True, default=None)
    owner = relationship(UserModel)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    session = relationship(SessionModel)
    sold = Column(Boolean, default=False)
    passed = Column(Boolean, default=False)
    row = Column(Integer, nullable=False)
    column = Column(Integer, nullable=False)

    def save_to_db(self):
        db_session.add(self)
        db_session.commit()

    @classmethod
    def generage_tickets_for_session(cls, session_id: int):
        session = SessionModel.find_by_id(id=session_id, to_dict=False)
        if session:
            for row in range(session.hall.rows):
                for column in range(session.hall.columns):
                    ticket = TicketModel(
                        session_id=session_id,
                        row=row + 1,
                        column=column + 1,
                        price=session.tickets_price,
                    )
                    ticket.save_to_db()
            return "Created"
        return "Session not found"

    @classmethod
    def reserve_ticket(cls, session_id: int, row: int, column: int, owner_id: int):
        ticket = db_session.query(cls).\
            filter_by(session_id=session_id, row=row, column=column).first()


        if ticket:
            if ticket.sold or ticket.owner_id:
                return "Ticket already reserved"
            ticket.sold = True
            ticket.owner_id = owner_id
            ticket.save_to_db()
            return "Reserved"
        return "Ticket not found"

    @classmethod
    def get_sold_tickets_for_session(cls, session_id: int, to_dict: bool = False):
        tickets = (
            db_session.query(cls).filter_by(session_id=session_id, sold=True).all()
        )
        if not tickets:
            return {}
        if to_dict:
            return [cls.to_dict(ticket) for ticket in tickets]
        else:
            return tickets

    @classmethod
    def find_by_id(cls, id, to_dict=False):
        ticket = db_session.query(cls).filter_by(id=id).first()
        if not ticket:
            return {}
        if to_dict:
            return cls.to_dict(ticket)
        else:
            return ticket

    @classmethod
    def find_by_owner_id(cls, owner_id, to_dict=False):
        tickets = db_session.query(cls).filter_by(owner_id=owner_id).all()
        if not tickets:
            return {}
        if to_dict:
            return [cls.to_dict(ticket) for ticket in tickets]
        else:
            return tickets

    @classmethod
    def find_by_session_id(cls, session_id, to_dict=False):
        tickets = (
            db_session.query(cls)
            .filter_by(session_id=session_id)
            .order_by(cls.row, cls.column)
            .all()
        )
        if not tickets:
            return {}
        if to_dict:
            return [cls.to_dict(ticket) for ticket in tickets]
        else:
            return tickets

    @classmethod
    def return_all_active(cls, to_dict=False):
        tickets = db_session.query(cls).filter_by(passed=False).order_by(cls.id).all()
        if to_dict:
            return [cls.to_dict(ticket) for ticket in tickets]
        else:
            return list(tickets)

    @classmethod
    def return_all_sold(cls, to_dict=False):
        tickets = db_session.query(cls).filter_by(sold=True).order_by(cls.id).all()
        if to_dict:
            return [cls.to_dict(ticket) for ticket in tickets]
        else:
            return list(tickets)

    @staticmethod
    def to_dict(ticket):
        if not ticket.passed:
            return {
                "id": ticket.id,
                "price": ticket.price,
                "owner_id": ticket.owner_id,
                "session_id": ticket.session_id,
                "sold": ticket.sold,
                "passed": ticket.passed,
                "row": ticket.row,
                "column": ticket.column,
            }
        else:
            return {"message": "Ticket was passed"}
