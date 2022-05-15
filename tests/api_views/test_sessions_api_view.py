import json
import datetime

from flask import url_for

from cinema import models

def test_get_sessions(app,client, create_session, session_factory, create_movie):
    movie = create_movie
    session1 = create_session
    session2 = session_factory(
        movie_id=movie.id,
        hall_id=session1.hall_id,
        date=datetime.date(year=2022, month=1, day=2),
        start_at="15:00:00",
        end_at="17:00:00",
        tickets_price=150,
    )
    session2.save_to_db()
    response = client.get(url_for("sessions_api.get_sessions"))
    assert response.status_code == 200
    for session in response.json:
        assert session["movie_id"]
        assert session["hall_id"]
        assert session["date"]
        assert session["end_at"]
        assert session["start_at"]
        assert session["tickets_price"]


def test_get_session(app,client, create_session):
    session = create_session
    response = client.get(url_for("sessions_api.get_session", session_id=session.id))
    res = response.json
    assert response.status_code == 200
    assert res["id"] == session.id
    assert res["movie_id"] == session.movie_id
    assert res["hall_id"] == session.hall_id
    assert res["date"] == json.dumps(session.date, default=str).strip('"')
    assert res["start_at"] == json.dumps(session.start_at, default=str).strip( '"')
    assert res["end_at"] == json.dumps(session.end_at, default=str).strip( '"')


def test_get_session_by_not_exist_id(app,client):
    response = client.get(url_for("sessions_api.get_session", session_id=9999))
    assert response.status_code == 404
    assert response.json["message"] == "Session not found."
