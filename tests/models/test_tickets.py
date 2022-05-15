from cinema import models


def test_ticket_create():
    ticket = models.TicketModel(
        price=100, owner_id=1, session_id=1, sold=True, passed=False, row=3, column=3
    )
    assert ticket.price == 100
    assert ticket.owner_id == 1
    assert ticket.session_id == 1
    assert ticket.sold == True
    assert ticket.passed == False
    assert ticket.row == 3
    assert ticket.row == 3


def test_find_by_id(create_ticket):
    ticket = create_ticket
    res = models.TicketModel.find_by_id(id=ticket.id)
    assert res == ticket


def test_find_by_not_extist_id():
    res = models.TicketModel.find_by_id(id=9999)
    assert res == {}


def test_find_by_owner_id(create_ticket, ticket_factory):
    ticket1 = create_ticket
    ticket2 = ticket_factory(
        price=100,
        owner_id=ticket1.owner_id,
        session_id=ticket1.session_id,
        sold=True,
        passed=False,
        row=1,
        column=2,
    )
    ticket2.save_to_db()
    res = models.TicketModel.find_by_owner_id(owner_id=ticket1.owner_id)
    assert ticket1 in res
    assert ticket2 in res


def test_find_by_not_exist_owner_id():
    res = models.TicketModel.find_by_owner_id(owner_id=9999)
    assert res == {}


def test_find_by_session_id(create_ticket, ticket_factory):
    ticket1 = create_ticket
    ticket2 = ticket_factory(
        price=100,
        owner_id=ticket1.owner_id,
        session_id=ticket1.session_id,
        sold=True,
        passed=False,
        row=1,
        column=2,
    )
    ticket2.save_to_db()
    res = models.TicketModel.find_by_session_id(session_id=ticket1.session_id)
    assert ticket1 in res
    assert ticket2 in res


def test_find_by_not_exist_owner_id():
    res = models.TicketModel.find_by_session_id(session_id=9999)
    assert res == {}


def test_return_all_active_tickets(create_ticket, ticket_factory):
    ticket1 = create_ticket
    ticket2 = ticket_factory(
        price=150,
        owner_id=ticket1.owner_id,
        session_id=ticket1.session_id,
        sold=True,
        passed=True,
        row=2,
        column=2,
    )
    ticket2.save_to_db()
    tickets = models.TicketModel.return_all_active()
    assert ticket1 in tickets
    assert ticket2 not in tickets


def test_return_all_sold_tickets( create_ticket, ticket_factory):
    ticket1 = create_ticket
    ticket2 = ticket_factory(
        price=150,
        owner_id=ticket1.owner_id,
        session_id=ticket1.session_id,
        sold=False,
        passed=False,
        row=3,
        column=3,
    )
    ticket2.save_to_db()
    tickets = models.TicketModel.return_all_sold()
    assert ticket1 in tickets
    assert ticket2 not in tickets


def test_to_dict_passed_ticket(create_ticket):
    ticket = create_ticket
    ticket.passed = True
    ticket.save_to_db()
    res = models.TicketModel.to_dict(ticket)

    assert res["message"] == "Ticket was passed"


def test_to_dict_not_passed_ticket(ticket_factory):
    ticket = ticket_factory(
        price=150, owner_id=1, session_id=1, sold=False, passed=False, row=2, column=2
    )
    res = models.TicketModel.to_dict(ticket)

    assert res["id"] == ticket.id
    assert res["price"] == ticket.price
    assert res["owner_id"] == ticket.owner_id
    assert res["session_id"] == ticket.session_id
    assert res["sold"] == ticket.sold
    assert res["passed"] == ticket.passed
    assert res["row"] == ticket.row
    assert res["column"] == ticket.column


def test_reserve_ticket(create_session, create_user):
    owner = create_user
    session = create_session
    ticket = models.TicketModel(
        price=100,
        owner_id=None,
        session_id=session.id,
        sold=False,
        passed=False,
        row=10,
        column=10,
    )
    ticket.save_to_db()
    message = models.TicketModel.reserve_ticket(
        session_id=session.id, owner_id=owner.id, row=10, column=10
    )

    assert ticket.sold == True
    assert ticket.owner_id == owner.id


def test_reserve_not_exist_ticket():
    message = models.TicketModel.reserve_ticket(
        session_id=999, owner_id=999, row=999, column=999
    )
    assert message == "Ticket not found"


def test_reserve_already_reserve_ticket(create_session, create_user):
    owner = create_user
    session = create_session
    ticket = models.TicketModel(
        price=100,
        owner_id=owner.id,
        session_id=session.id,
        sold=True,
        passed=False,
        row=1,
        column=1,
    )
    ticket.save_to_db()
    message = models.TicketModel.reserve_ticket(
        session_id=session.id, owner_id=owner.id, row=1, column=1
    )
    assert message == "Ticket already reserved"
    assert ticket.sold == True
    assert ticket.owner_id == owner.id
