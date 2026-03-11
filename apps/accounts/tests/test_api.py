import pytest


pytestmark = pytest.mark.django_db


def test_user_can_register_and_receive_token(api_client):
	response = api_client.post(
		"/api/accounts/",
		{
			"first_name": "Test",
			"last_name": "User",
			"email": "new@example.com",
			"phone_number": "123456789",
			"country": "EG",
			"password": "password123",
		},
		format="multipart",
	)

	assert response.status_code == 201
	assert "token" in response.data
	assert response.data["email"] == "new@example.com"


def test_user_can_login_and_receive_token(api_client, user):
	response = api_client.post(
		"/api/accounts/login/",
		{"email": user.email, "password": "password123"},
		format="json",
	)

	assert response.status_code == 200
	assert response.data["id"] == user.id
	assert "token" in response.data


def test_non_admin_list_returns_only_self(auth_client, user, other_user):
	response = auth_client.get("/api/accounts/")

	assert response.status_code == 200
	assert len(response.data) == 1
	assert response.data[0]["id"] == user.id


def test_non_admin_cannot_fetch_other_user_detail(auth_client, other_user):
	response = auth_client.get(f"/api/accounts/{other_user.id}/")

	assert response.status_code == 404


def test_admin_list_returns_all_users(admin_client, user, other_user, admin_user):
	response = admin_client.get("/api/accounts/")

	assert response.status_code == 200
	returned_ids = {item["id"] for item in response.data}
	assert returned_ids == {user.id, other_user.id, admin_user.id}
