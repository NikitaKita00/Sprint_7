import pytest
import httpx
import random
import string

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"


def generate_order_data(color=None):
    """Генерирует тело запроса для создания заказа, с опциональным цветом"""
    return {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "Saske, come back to Konoha",
        "color": color if color is not None else [],
    }


def create_order(order_data):

    with httpx.Client() as client:
        response = client.post(f"{BASE_URL}/orders", json=order_data)
    return response


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
