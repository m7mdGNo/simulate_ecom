import pytest


pytestmark = pytest.mark.django_db


def test_products_list_is_public(api_client, product):
	response = api_client.get("/api/products/")

	assert response.status_code == 200
	assert len(response.data) == 1
	assert response.data[0]["id"] == product.id


def test_anonymous_user_cannot_create_product(api_client):
	response = api_client.post(
		"/api/products/",
		{"name": "Orange", "category": "Fruits", "description": "Sweet"},
		format="json",
	)

	assert response.status_code == 401


def test_regular_user_cannot_create_product(auth_client):
	response = auth_client.post(
		"/api/products/",
		{"name": "Orange", "category": "Fruits", "description": "Sweet"},
		format="json",
	)

	assert response.status_code == 403


def test_admin_can_create_product(admin_client):
	response = admin_client.post(
		"/api/products/",
		{"name": "Orange", "category": "Fruits", "description": "Sweet"},
		format="json",
	)

	assert response.status_code == 201
	assert response.data["name"] == "Orange"
