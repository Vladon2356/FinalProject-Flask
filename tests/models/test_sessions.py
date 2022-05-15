import datetime, json

from cinema import models


def test_session_create(app):
    session = models.SessionModel(
        movie_id=1,
        hall_id=1,
        date=datetime.date(year=2022, month=1, day=1),
        start_at="15:00:00",
        end_at="17:00:00",
        tickets_price=100,
    )
    assert session.movie_id == 1
    assert session.hall_id == 1
    assert session.date == datetime.date(year=2022, month=1, day=1)
    assert session.start_at == "15:00:00"
    assert session.end_at == "17:00:00"
    assert session.tickets_price == 100


def test_session_create():
    session = models.SessionModel(
        movie_id=1,
        hall_id=1,
        date=datetime.date(year=2022, month=1, day=1),
        start_at="15:00:00",
        end_at="17:00:00",
        tickets_price=100,
    )
    assert session.movie_id == 1
    assert session.hall_id == 1
    assert session.date == datetime.date(year=2022, month=1, day=1)
    assert session.start_at == "15:00:00"
    assert session.end_at == "17:00:00"
    assert session.tickets_price == 100


def test_find_by_id(create_session):
    session = create_session
    res = models.SessionModel.find_by_id(id=session.id)
    assert res == session


def test_find_by_not_extist_id():
    res = models.SessionModel.find_by_id(id=9999)
    assert res == {}


def test_find_by_movie_id( create_session, session_factory):
    session1 = create_session
    session2 = session_factory(
        movie_id=session1.movie_id,
        hall_id=session1.hall_id,
        date=datetime.date(year=2022, month=1, day=1),
        start_at="15:00:00",
        end_at="17:00:00",
        tickets_price=100,
    )
    session2.save_to_db()
    res = models.SessionModel.find_by_movie_id(movie_id=session1.movie_id)
    assert session1 in res
    assert session2 in res


def test_find_by_not_exist_movie_id():
    res = models.SessionModel.find_by_movie_id(movie_id=9999)
    assert res == {}


def test_return_all_sessions( create_session, session_factory):
    session1 = create_session
    session2 = session_factory(
        movie_id=session1.movie_id,
        hall_id=session1.hall_id,
        date=datetime.date(year=2022, month=1, day=1),
        start_at="15:00:00",
        end_at="17:00:00",
        tickets_price=100,
    )
    session2.save_to_db()
    sessions = models.SessionModel.return_all()
    assert session1 in sessions
    assert session2 in sessions


def test_to_dict_not_active_session( create_session):
    session = create_session
    session.is_active = False
    session.save_to_db()
    res = models.SessionModel.to_dict(session)

    assert res["message"] == "Session was deleted"


def test_to_dict_active_session( session_factory,create_movie, create_hall):
    movie = create_movie
    hall = create_hall
    session = session_factory(
        movie_id=movie.id,
        hall_id=hall.id,
        date=datetime.date(year=2022, month=1, day=1),
        start_at="15:00:00",
        end_at="17:00:00",
        tickets_price=100,
    )
    res = models.SessionModel.to_dict(session)

    assert res["id"] == session.id
    assert res["movie_id"] == session.movie_id
    assert res["hall_id"] == session.hall_id
    assert res["date"] == json.dumps(session.date, default=str).strip('"')
    assert res["start_at"] == json.dumps(session.start_at, default=str).strip('"')
    assert res["end_at"] == json.dumps(session.end_at, default=str).strip('"')


def test_delete_by_id( create_session):
    session = create_session
    code = models.SessionModel.delete_by_id(session.id)
    assert code == 200


def test_delete_by_not_exist_id():
    code = models.SessionModel.delete_by_id(9999)
    assert code == 404


def test_for_search_by_movie_id( create_session_for_search):
    session, session2, session3, session4 = create_session_for_search
    res = models.SessionModel.for_search(movie_id=1)
    for item in res:
        assert item.movie_id == 1


def test_for_search_by_date( create_session_for_search):
    session, session2, session3, session4 = create_session_for_search
    res = models.SessionModel.for_search(date=datetime.date(year=2022, month=1, day=1))
    for item in res:
        assert item.date == datetime.date(year=2022, month=1, day=1)


def test_for_search_by_all_params( create_session_for_search):
    session, session2, session3, session4 = create_session_for_search
    res = models.SessionModel.for_search(
        movie_id=session2.movie_id,
        date=datetime.date(year=2022, month=1, day=1),
        genres="Fantasy",
        actors="Chris Hemsworth",
        producer="Taika Waititi",
    )
    for item in res:
        assert item.movie_id == session2.movie_id
        assert item.date == datetime.date(year=2022, month=1, day=1)
        assert "Fantasy" in item.movie.genres
        assert "Chris Hemsworth" in item.movie.actors
        assert "Taika Waititi" in item.movie.producer


def test_for_search_by_not_extist_params( create_session_for_search):
    session, session2, session3, session4 = create_session_for_search
    res = models.SessionModel.for_search(
        movie_id=9999,
        date=datetime.date(year=2022, month=2, day=2),
        genres="Test",
        actors="Test",
        producer="Test",
    )
    assert res == {}
