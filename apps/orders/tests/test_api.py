import pytest


pytestmark = pytest.mark.django_db


def test_user_lists_only_own_orders(auth_client, order, other_order):
	response = auth_client.get("/api/orders/")

	assert response.status_code == 200
	assert len(response.data) == 1
	assert response.data[0]["id"] == order.id


def test_admin_lists_all_orders(admin_client, order, other_order):
	response = admin_client.get("/api/orders/")

	assert response.status_code == 200
	returned_ids = {item["id"] for item in response.data}
	assert returned_ids == {order.id, other_order.id}


def test_create_order_uses_authenticated_user(auth_client, user, other_user):
	response = auth_client.post(
		"/api/orders/",
		{"user": other_user.id, "address": "Test address"},
		format="json",
	)

	assert response.status_code == 201
	assert response.data["user"] == user.id


def test_user_lists_only_own_order_items(auth_client, order_item, other_order_item):
	response = auth_client.get("/api/orders/items/")

	assert response.status_code == 200
	assert len(response.data) == 1
	assert response.data[0]["id"] == order_item.id


def test_admin_lists_all_order_items(admin_client, order_item, other_order_item):
	response = admin_client.get("/api/orders/items/")

	assert response.status_code == 200
	returned_ids = {item["id"] for item in response.data}
	assert returned_ids == {order_item.id, other_order_item.id}
