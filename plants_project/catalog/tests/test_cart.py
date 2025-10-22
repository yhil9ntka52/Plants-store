import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from catalog.models import Plant, Category, Cart

@pytest.fixture
def category(db):
    return Category.objects.create(name="Test Category")

@pytest.fixture
def plant(category):
    return Plant.objects.create(
        name="Rose",
        price=100,
        category=category
    )

@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(username="testuser", password="pass")

@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client

@pytest.fixture
def cart_item(user, plant):
    return Cart.objects.create(user=user, plant=plant, quantity=2)

def test_cart_list_empty(auth_client):
    response = auth_client.get("/api/v1/catalog/cart/")
    assert response.status_code == 200
    assert response.data == []

def test_cart_add(auth_client, plant):
    data = {"plant": plant.id, "quantity": 3}
    response = auth_client.post("/api/v1/catalog/cart/", data)
    assert response.status_code == 201
    assert response.data["plant"] == plant.id
    assert response.data["quantity"] == 3

def test_cart_add_invalid(auth_client):
    data = {"plant": 999999, "quantity": 3}
    response = auth_client.post("/api/v1/catalog/cart/", data)
    assert response.status_code in [400, 404]

def test_cart_delete(auth_client, cart_item):
    response = auth_client.delete(f"/api/v1/catalog/cart/{cart_item.id}/")
    assert response.status_code == 204

def test_cart_delete_not_found(auth_client):
    response = auth_client.delete("/api/v1/catalog/cart/9999/")
    assert response.status_code == 404

def test_cart_list_unauthorized(db):
    client = APIClient()
    response = client.get("/api/v1/catalog/cart/")
    assert response.status_code in [401, 403, 404]

def test_empty_cart_checkout(auth_client):
    response = auth_client.post("/api/v1/catalog/cart/checkout/")
    assert response.status_code in [400, 404]
    if response.status_code == 400:
        assert "empty" in response.data.get("error", "")
