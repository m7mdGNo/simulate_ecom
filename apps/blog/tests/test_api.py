import pytest


pytestmark = pytest.mark.django_db


def test_blogs_require_authentication(api_client):
	response = api_client.get("/api/blogs/")

	assert response.status_code == 401


def test_user_lists_only_own_blogs(auth_client, blog, other_blog):
	response = auth_client.get("/api/blogs/")

	assert response.status_code == 200
	assert len(response.data) == 1
	assert response.data[0]["id"] == blog.id


def test_admin_lists_all_blogs(admin_client, blog, other_blog):
	response = admin_client.get("/api/blogs/")

	assert response.status_code == 200
	returned_ids = {item["id"] for item in response.data}
	assert returned_ids == {blog.id, other_blog.id}


def test_create_blog_uses_authenticated_user(auth_client, user, other_user):
	response = auth_client.post(
		"/api/blogs/",
		{"user": other_user.id, "name": "New blog", "content": "Body"},
		format="json",
	)

	assert response.status_code == 201
	assert response.data["user"] == user.id
