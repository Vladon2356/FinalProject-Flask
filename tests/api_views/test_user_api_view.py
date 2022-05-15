from flask import url_for


def test_get_users(app, client, create_user, authentication_headers):
    user = create_user
    response = client.get(
        url_for("users_api.get_users"), headers=authentication_headers(is_admin=True)
    )
    assert response.status_code == 200
    for user in response.json:
        assert user["id"]
        assert user["first_name"]
        assert user["last_name"]
        assert user["age"]
        assert user["email"]
        assert user["is_active"]



def test_get_users_by_not_admin(app, client, create_user, authentication_headers):
    user = create_user
    response = client.get(
        url_for("users_api.get_user", user_id=user.id),
        headers=authentication_headers(is_admin=False),
    )
    res = response.json
    assert response.status_code == 403
    assert res["message"] == "Forbidden"


def test_get_user(app, client, create_user, authentication_headers):
    user = create_user
    response = client.get(
        url_for("users_api.get_user", user_id=user.id),
        headers=authentication_headers(is_admin=True),
    )
    res = response.json
    assert response.status_code == 200
    assert res["id"] == user.id
    assert res["first_name"] == user.first_name
    assert res["last_name"] == user.last_name
    assert res["age"] == user.age
    assert res["email"] == user.email
    assert res["is_active"] == user.is_active
    assert res["is_admin"] == user.is_admin


def test_get_user_by_not_admin(app, client, create_user, authentication_headers):
    user = create_user
    response = client.get(
        url_for("users_api.get_user", user_id=user.id),
        headers=authentication_headers(is_admin=False),
    )
    res = response.json
    assert response.status_code == 403
    assert res["message"] == "Forbidden"


def test_get_me(app,client, authentication_headers):
    response = client.get(
        url_for("users_api.get_me"), headers=authentication_headers(is_admin=True)
    )
    res = response.json
    assert response.status_code == 200
    assert res["first_name"] == "Test"
    assert res["last_name"] == "Admin"
    assert res["age"] == 22
    assert res["email"] == "test@gmail.com"
    assert res["is_active"] == True
    assert res["is_admin"] == True


def test_get_me_without_login(app, client):
    response = client.get(
        url_for("users_api.get_me"),
    )
    assert response.status_code == 401
    assert response.json["msg"] == "Missing Authorization Header"
