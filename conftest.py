import pytest
from helpers import (
    generate_unique_courier,
    create_courier,
    login_courier,
    delete_courier,
    generate_order_data,
)


@pytest.fixture(scope="function")
def courier():
    data = generate_unique_courier()
    response = create_courier(data)
    assert response.status_code == 201

    yield data

    login_resp = login_courier({"login": data["login"], "password": data["password"]})
    if login_resp and login_resp.status_code == 200:
        courier_id = login_resp.json().get("id")
        delete_courier(courier_id)


@pytest.fixture(
    params=[
        None,
        {"page": 0},
        {"limit": 10},
        {"page": 1, "limit": 5},
        {"nearestStation": '["1","2"]'},
        {"courierId": 12345},  # Пример несуществующего курьера
    ]
)
def order_params(request):
    return request.param


@pytest.fixture(params=[["BLACK"], ["GREY"], ["BLACK", "GREY"], [], None])
def order_data(request):
    return generate_order_data(color=request.param)


@pytest.fixture(scope="function")
def courier_data():
    data = generate_unique_courier()
    response = create_courier(data)
    assert response.status_code == 201
    yield data
    login_resp = login_courier({"login": data["login"], "password": data["password"]})
    if login_resp and login_resp.status_code == 200:
        courier_id = login_resp.json().get("id")
        delete_courier(courier_id)


class TestCourierCreate:
    def test_create_courier_success(self, courier_data):
        response = create_courier(courier_data)
        assert response.status_code == 201
        assert response.json() == {"ok": True}

    def test_create_duplicate_courier_should_fail(self, courier_data):
        response1 = create_courier(courier_data)
        assert response1.status_code == 201

        response2 = create_courier(courier_data)
        assert response2.status_code == 409
        assert "Этот логин уже используется" in response2.json().get("message", "")

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_required_field(self, courier_data, missing_field):
        incomplete_data = courier_data.copy()
        incomplete_data.pop(missing_field)
        response = create_courier(incomplete_data)
        assert response.status_code == 400
        assert "Недостаточно данных" in response.json().get("message", "")