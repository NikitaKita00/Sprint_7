import pytest
from helpers import get_orders  # Предполагается, что get_orders вынесена в helpers.py


@pytest.mark.parametrize(
    "params",
    [
        None,
        {"page": 0},
        {"limit": 10},
        {"page": 1, "limit": 5},
        {"nearestStation": '["1","2"]'},
        {"courierId": 12345},  # Пример несуществующего курьера
    ],
)
def test_get_orders_list(params):
    response = get_orders(params)
    if response.status_code == 404:
        json_resp = response.json()
        if "Курьер с идентификатором" in json_resp.get("message", ""):
            pytest.skip(f"Courier ID {params['courierId']} not found, skipping test")
        else:
            pytest.fail(f"Unexpected 404 error: {response.text}")
    else:
        assert (
            response.status_code == 200
        ), f"Unexpected status code: {response.status_code}, body: {response.text}"
        json_resp = response.json()
        assert "orders" in json_resp, f"Response missing 'orders' key: {response.text}"
        assert isinstance(
            json_resp["orders"], list
        ), f"'orders' is not a list: {response.text}"
