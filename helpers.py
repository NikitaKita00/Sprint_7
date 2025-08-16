import random
import string
import httpx

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


def safe_post(url, json, max_retries=3):
    last_exception = None
    for attempt in range(max_retries):
        try:
            with httpx.Client() as client:
                response = client.post(url, json=json)
                if response.status_code < 500:
                    return response
        except (httpx.ReadTimeout, httpx.ConnectTimeout, httpx.RequestError) as exc:
            last_exception = exc
    return None

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

def get_orders(params=None):
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/orders", params=params)
    return response

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