import pytest
import allure
from helpers import generate_order_data, create_order


@allure.title("Создание заказа с разными цветами")
@allure.description("Проверяется успешное создание заказа с разными вариантами цвета")
@pytest.mark.parametrize(
    "colors",
    [
        (["BLACK"]),
        (["GREY"]),
        (["BLACK", "GREY"]),
        ([]),
        (None),
    ],
)
def test_create_order_with_different_colors(colors):
    order_data = generate_order_data(color=colors)
    response = create_order(order_data)
    assert (
        response.status_code == 201
    ), f"Unexpected status: {response.status_code}, body: {response.text}"
    json_resp = response.json()
    assert "track" in json_resp, f"Response missing 'track': {json_resp}"
