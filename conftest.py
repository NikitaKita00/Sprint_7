import pytest
from helpers import (
    generate_unique_courier,
    create_courier,
    login_courier,
    delete_courier,
    create_order,
    generate_order_data,
)


@pytest.fixture
def courier_data():
    return generate_unique_courier()


@pytest.fixture(scope="function")
def created_courier(courier_data):
    response = create_courier(courier_data)
    assert response.status_code == 201
    yield courier_data
    login_resp = login_courier(
        {"login": courier_data["login"], "password": courier_data["password"]}
    )
    if login_resp and login_resp.status_code == 200:
        courier_id = login_resp.json().get("id")
        delete_courier(courier_id)


@pytest.fixture
def created_order(order_data_fixture):
    response = create_order(order_data_fixture)
    assert response.status_code == 201
    yield response
