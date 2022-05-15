from cinema import models


def test_hall_create():
    hall = models.HallModel(
        title="Test",
        rows=10,
        columns=10,
    )
    assert hall.title == "Test"
    assert hall.rows == 10
    assert hall.columns == 10


def test_find_by_id(create_hall):
    hall = create_hall
    res = models.HallModel.find_by_id(id=hall.id)
    assert res == hall


def test_find_by_not_extist_id():
    res = models.HallModel.find_by_id(id=9999)
    assert res == {}


def test_return_all(create_hall, hall_factory):
    hall1 = create_hall
    hall2 = hall_factory(title="TestHall", columns=10, rows=10)
    hall2.save_to_db()
    res = models.HallModel.return_all()
    assert hall1 in res
    assert hall2 in res


def test_delete_by_id(create_hall):
    hall = create_hall
    code = models.HallModel.delete_by_id(id=hall.id)
    assert code == 200


def test_delete_by_not_exist_id():
    code = models.HallModel.delete_by_id(id=9999)
    assert code == 404


def test_to_dict_hall(create_hall):
    hall = create_hall
    res = models.HallModel.to_dict(hall)

    assert res["id"] == hall.id
    assert res["title"] == hall.title
    assert res["rows"] == hall.rows
    assert res["columns"] == hall.columns
