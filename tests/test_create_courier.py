import pytest
import allure
from helpers import create_courier


class TestCourierCreate:
    @allure.title("Успешное создание курьера")
    @allure.description(
        "Проверяет, что курьер успешно создаётся (201) и возвращается {'ok': True}"
    )
    def test_create_courier_success(self, courier_data):
        response = create_courier(courier_data)
        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.title("Создание дубликатного курьера возвращает ошибку")
    @allure.description(
        "Попытка создать курьера с уже существующим логином даёт 409 Conflict и сообщение"
    )
    def test_create_duplicate_courier_should_fail(self, created_courier):
        # Первый вызов уже сделал фикстура created_courier
        response2 = create_courier(created_courier)
        assert response2.status_code == 409
        assert "Этот логин уже используется" in response2.json().get("message", "")

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    @allure.title("Создание курьера с отсутствующим обязательным полем")
    @allure.description("Проверка ошибки 400 при отсутствии обязательного поля")
    def test_create_courier_missing_required_field(self, courier_data, missing_field):
        incomplete_data = courier_data.copy()
        incomplete_data.pop(missing_field)
        response = create_courier(incomplete_data)
        assert response.status_code == 400
        assert "Недостаточно данных" in response.json().get("message", "")
