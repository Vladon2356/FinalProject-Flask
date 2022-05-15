import os
import datetime

import pytest
from flask import url_for
from dotenv import load_dotenv

from cinema import models
from config import BaseConfig

load_dotenv()

BaseConfig.SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DB_URI")

TEST_FIRST_NAME = "Test"
TEST_LAST_NAME = "User"
TEST_PASSWORD = "test1234"
ADMIN_TEST_FIRST_NAME = "Test"
ADMIN_TEST_LAST_NAME = "Admin"
ADMIN_TEST_PASSWORD = "admin123"


@pytest.fixture(scope="session")
def app():
    from cinema.main import create_app, clear_database

    clear_database()
    app = create_app(BaseConfig)
    app.testing = True
    ctx = app.app_context()
    ctx.push()
    yield app
    ctx.pop


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def authentication_headers(client):
    def wrapper(is_admin: bool):
        first_name = ADMIN_TEST_FIRST_NAME if is_admin else TEST_FIRST_NAME
        last_name = ADMIN_TEST_LAST_NAME if is_admin else TEST_LAST_NAME
        password = ADMIN_TEST_PASSWORD if is_admin else TEST_PASSWORD
        response = client.post(
            url_for('auth_api.login'),
            json={
                "first_name": first_name,
                "last_name": last_name,
                "password": password
            }
        )

        if response.json['message'] == f"User {first_name} {last_name} doesn't exist":
            response = client.post(
                url_for("auth_api.register"),
                json={
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": "test@gmail.com",
                    "age": 22,
                    "password": password,
                    "is_admin": is_admin,
                },
            )
        auth_token = response.json["access_token"]
        refresh_token = response.json["refresh_token"]
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "refresh_token": refresh_token,
        }

        return headers

    return wrapper


@pytest.fixture(scope="session")
def create_user():
    user = models.UserModel(
        first_name="Test",
        last_name="Test",
        email="test@gmail.com",
        age=22,
        hashed_password=models.UserModel.generate_hash("123"),
        is_admin=True,
        is_active=True,
    )
    user.save_to_db()
    return user


@pytest.fixture(scope="session")
def create_ticket(create_session, create_user):
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
    return ticket


@pytest.fixture(scope="session")
def create_movie():
    movie = models.MovieModel(
        title="TestTitle",
        description="Something",
        year=2022,
        duration=123,
        genres="Fantasy, Marvel",
        actors="Tom Hardy",
        producer="Kevin Faigy",
        age_rating="G",
        in_rental=True,
    )
    movie.save_to_db()
    return movie


@pytest.fixture(scope="session")
def create_hall():
    hall = models.HallModel(title="Main", rows=10, columns=10)
    hall.save_to_db()
    return hall


@pytest.fixture(scope="session")
def create_session(create_hall, create_movie):
    movie = create_movie
    hall = create_hall
    session = models.SessionModel(
        movie_id=movie.id,
        hall_id=hall.id,
        date=datetime.date(year=2022, month=1, day=1),
        start_at="15:00:00",
        end_at="17:00:00",
        tickets_price=100,
    )
    session.save_to_db()
    return session


@pytest.fixture(scope="session")
def create_session_for_search(create_hall, create_movie):
    movie = create_movie
    movie2 = models.MovieModel(
        title="TestTitle2",
        description="Something2",
        year=2022,
        duration=140,
        genres="Fantasy, Horror",
        actors="Chris Hemsworth, Tom Holland",
        producer="Taika Waititi",
        age_rating="G",
        in_rental=True,
    )
    movie2.save_to_db()
    hall = create_hall
    session = models.SessionModel(
        movie_id=movie.id,
        hall_id=hall.id,
        date=datetime.date(year=2022, month=1, day=1),
        start_at="15:00:00",
        end_at="17:00:00",
        tickets_price=100,
    )
    session2 = models.SessionModel(
        movie_id=movie2.id,
        hall_id=hall.id,
        date=datetime.date(year=2022, month=1, day=1),
        start_at="15:00:00",
        end_at="17:00:00",
        tickets_price=100,
    )
    session3 = models.SessionModel(
        movie_id=movie2.id,
        hall_id=hall.id,
        date=datetime.date(year=2022, month=1, day=2),
        start_at="15:00:00",
        end_at="17:00:00",
        tickets_price=100,
    )
    session4 = models.SessionModel(
        movie_id=movie.id,
        hall_id=hall.id,
        date=datetime.date(year=2022, month=1, day=2),
        start_at="15:00:00",
        end_at="17:00:00",
        tickets_price=100,
    )
    session.save_to_db()
    session2.save_to_db()
    session3.save_to_db()
    session4.save_to_db()
    return session, session2, session3, session4


@pytest.fixture(scope="session")
def user_factory():
    def _user_factory(
        first_name, last_name, email, age, hashed_password, is_admin, is_active
    ):
        new_user = models.UserModel(
            first_name=first_name,
            last_name=last_name,
            email=email,
            age=age,
            hashed_password=hashed_password,
            is_admin=is_admin,
            is_active=is_active,
        )
        new_user.save_to_db()

        return new_user

    return _user_factory


@pytest.fixture(scope="session")
def movie_factory():
    def _movie_factory(
        title,
        description,
        year,
        duration,
        genres,
        actors,
        producer,
        age_rating,
        in_rental,
    ):
        new_movie = models.MovieModel(
            title=title,
            description=description,
            year=year,
            duration=duration,
            genres=genres,
            actors=actors,
            producer=producer,
            age_rating=age_rating,
            in_rental=in_rental,
        )
        new_movie.save_to_db()

        return new_movie

    return _movie_factory


@pytest.fixture(scope="session")
def session_factory():
    def _session_factory(
        movie_id, hall_id, date, start_at, end_at, tickets_price, *args, **kwargs
    ):
        new_session = models.SessionModel(
            movie_id=movie_id,
            hall_id=hall_id,
            date=date,
            start_at=start_at,
            end_at=end_at,
            tickets_price=tickets_price,
        )
        new_session.save_to_db()

        return new_session

    return _session_factory


@pytest.fixture(scope="session")
def ticket_factory():
    def _ticket_factory(price, owner_id, session_id, sold, passed, row, column):
        new_ticket = models.TicketModel(
            price=price,
            owner_id=owner_id,
            session_id=session_id,
            sold=sold,
            passed=passed,
            row=row,
            column=column,
        )
        new_ticket.save_to_db()

        return new_ticket

    return _ticket_factory


@pytest.fixture(scope="session")
def hall_factory():
    def _hall_factory(title, rows, columns):
        new_hall = models.HallModel(title=title, rows=rows, columns=columns)
        new_hall.save_to_db()

        return new_hall

    return _hall_factory
