from cinema import models


def test_user_create():
    user = models.UserModel(
        first_name="Test",
        last_name="User",
        email="test@gmail.com",
        age=22,
        hashed_password=models.UserModel.generate_hash("123"),
        is_admin=True,
        is_active=True,
    )
    assert user.first_name == "Test"
    assert user.last_name == "User"
    assert user.email == "test@gmail.com"
    assert user.age == 22
    assert models.UserModel.verify_hash("123", user.hashed_password)
    assert user.is_admin == True
    assert user.is_active == True


def test_find_by_id(create_user):
    user1 = create_user
    user = models.UserModel.find_by_id(user1.id)
    assert user.id == user1.id
    assert user == user1


def test_find_by_wrong_id():
    user = models.UserModel.find_by_id(999)
    assert user == {}


def test_find_by_first_and_last_name(create_user):
    user1 = create_user
    user = models.UserModel.find_by_first_and_last_name(
        first_name=user1.first_name, last_name=user1.last_name, to_dict=False
    )
    assert user.first_name == user1.first_name
    assert user.last_name == user1.last_name


def test_find_by_not_extist_first_and_last_name(create_user):
    user1 = create_user
    user = models.UserModel.find_by_first_and_last_name(
        first_name="XXXXXXX", last_name="PPPPPP"
    )
    assert user == {}


def test_find_by_email(create_user):
    user1 = create_user
    user = models.UserModel.find_by_email(email="test@gmail.com")
    assert user.first_name == user1.first_name
    assert user.last_name == user1.last_name


def test_find_by_not_email(create_user):
    user1 = create_user
    user = models.UserModel.find_by_email(email="XXXXXXX")
    assert user == {}


def test_return_all(create_user, user_factory):
    user1 = create_user
    user2 = user_factory(
        first_name="Test",
        last_name="User",
        email="test@gmail.com",
        age=22,
        hashed_password=models.UserModel.generate_hash("123"),
        is_admin=True,
        is_active=True,
    )
    users = models.UserModel.return_all()
    assert user1 in users
    assert user2 in users


def test_users_return_all_is_active(create_user, user_factory):
    user = create_user
    user_not_active = user_factory(
        first_name="Test",
        last_name="User",
        email="test@gmail.com",
        age=22,
        hashed_password=models.UserModel.generate_hash("123"),
        is_admin=True,
        is_active=False,
    )
    users = models.UserModel.return_all_is_active()
    assert user in users
    assert user_not_active not in users


def test_delete_by_id(create_user):
    user1 = create_user
    code = models.UserModel.delete_by_id(user1.id)
    assert code == 200


def test_delete_by_not_exist_id():
    code = models.UserModel.delete_by_id(999)
    assert code == 404


def test_to_dict_for_user_not_is_active(user_factory):
    user = user_factory(
        first_name="Test",
        last_name="User",
        email="test@gmail.com",
        age=22,
        hashed_password=models.UserModel.generate_hash("123"),
        is_admin=True,
        is_active=False,
    )
    res = models.UserModel.to_dict(user)
    assert res["message"] == "User was deleted"


def test_to_dict_for_user_is_active(user_factory):
    user = user_factory(
        first_name="Test",
        last_name="User",
        email="test@gmail.com",
        age=22,
        hashed_password=models.UserModel.generate_hash("123"),
        is_admin=True,
        is_active=True,
    )
    res = models.UserModel.to_dict(user)

    assert res["id"] == user.id
    assert res["first_name"] == user.first_name
    assert res["last_name"] == user.last_name
    assert res["email"] == user.email
    assert res["is_admin"] == user.is_admin
    assert res["is_active"] == user.is_active
