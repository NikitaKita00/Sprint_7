import pytest
import httpx
import random
import string

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"


def generate_unique_courier():
    login = "".join(random.choices(string.ascii_letters + string.digits, k=8))
    password = "".join(random.choices(string.ascii_letters + string.digits, k=8))
    firstName = "TestName"
    return {"login": login, "password": password, "firstName": firstName}


def create_courier(data):
    with httpx.Client() as client:
        return client.post(f"{BASE_URL}/courier", json=data)


def login_courier(data):
    with httpx.Client() as client:
        return client.post(f"{BASE_URL}/courier/login", json=data)


def delete_courier(courier_id):
    with httpx.Client() as client:
        return client.delete(f"{BASE_URL}/courier/{courier_id}")


class TestCourierCreate:
    def setup_method(self):
        self.courier_data = generate_unique_courier()

    def teardown_method(self):
        login_resp = login_courier(
            {
                "login": self.courier_data["login"],
                "password": self.courier_data["password"],
            }
        )
        if login_resp.status_code == 200:
            courier_id = login_resp.json().get("id")
            delete_courier(courier_id)

    def test_create_courier_success(self):
        response = create_courier(self.courier_data)
        assert response.status_code == 201
        assert response.json() == {"ok": True}

    def test_create_duplicate_courier_should_fail(self):

        response1 = create_courier(self.courier_data)
        assert response1.status_code == 201

        response2 = create_courier(self.courier_data)
        assert response2.status_code == 409
        assert "Этот логин уже используется" in response2.json().get("message", "")

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_required_field(self, missing_field):
        incomplete_data = self.courier_data.copy()
        incomplete_data.pop(missing_field)
        response = create_courier(incomplete_data)
        assert response.status_code == 400
        assert "Недостаточно данных" in response.json().get("message", "")
