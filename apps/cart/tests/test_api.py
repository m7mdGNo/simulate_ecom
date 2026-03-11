import pytest


pytestmark = pytest.mark.django_db


def test_cart_requires_authentication(api_client):
	response = api_client.get("/api/cart/")

	assert response.status_code == 401


def test_user_lists_only_own_cart_items(auth_client, cart_item, other_cart_item):
	response = auth_client.get("/api/cart/")

	assert response.status_code == 200
	assert len(response.data) == 1
	assert response.data[0]["id"] == cart_item.id


def test_admin_lists_all_cart_items(admin_client, cart_item, other_cart_item):
	response = admin_client.get("/api/cart/")

	assert response.status_code == 200
	returned_ids = {item["id"] for item in response.data}
	assert returned_ids == {cart_item.id, other_cart_item.id}


def test_create_cart_item_uses_authenticated_user(auth_client, user, other_user, product):
	response = auth_client.post(
		"/api/cart/",
		{"user": other_user.id, "product": product.id, "quantity": 5},
		format="json",
	)

	assert response.status_code == 201
	assert response.data["user"] == user.id
