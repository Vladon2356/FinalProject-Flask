from flask import url_for


def test_login(app,client, create_user):
    user = create_user
    response = client.post(
        url_for("auth_api.login"),
        json={
            "first_name": user.first_name,
            "last_name": user.last_name,
            "password": "123",
        },
    )
    assert response.status_code == 200
    assert (
        response.json["message"] == f"Logged in as {user.first_name} "
        f"{user.last_name}"
    )


def test_login_with_wrong_data(app, client):
    response = client.post(
        url_for("auth_api.login"),
        json={"first_name": "XXX", "last_name": "XXXX", "password": "123"},
    )
    assert response.status_code == 200
    assert response.json["message"] == f"User XXX XXXX doesn't exist"


def test_login_without_data(app, client):
    response = client.post(url_for("auth_api.login"), json={})
    assert response.status_code == 400
    assert (
        response.json["message"] == f'Please, provide "first_name", '
        f'"last_name" and "password" in body.'
    )


def test_register(app,client):
    response = client.post(
        url_for("auth_api.register"),
        json={
            "first_name": "From",
            "last_name": "Test",
            "email": "test123@gmail.com",
            "age": 33,
            "password": "123",
            "is_admin": True,
        },
    )
    assert response.status_code == 200
    assert response.json["message"] == f"User From Test was created"


def test_register_without_data(app, client):
    response = client.post(url_for("auth_api.register"), json={})
    assert response.status_code == 400
    assert (
        response.json["message"] == f'Please, provide "age", "last_name",'
        f' first_name", "email" and "password" in body.'
    )


def test_register_exist_user(app,client, create_user):
    user = create_user
    response = client.post(
        url_for("auth_api.register"),
        json={
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": "test123@gmail.com",
            "age": 33,
            "password": "123",
            "is_admin": True,
        },
    )

    assert response.status_code == 200
    assert response.json["message"] == f"User with username - {user.first_name} "\
        f"{user.last_name} already exists"



def test_refresh( client, authentication_headers):
    refresh_token = authentication_headers(is_admin=False)['refresh_token']
    response = client.post(
        url_for("auth_api.refresh"), headers= {'Authorization': f'Bearer {refresh_token}'}
    )

    assert response.status_code == 200
    assert response.json["access_token"]
