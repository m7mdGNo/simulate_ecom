import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from accounts.models import User
from blog.models import Blog
from cart.models import Cart
from orders.models import Order, OrderItem
from products.models import Product


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="user@example.com",
        password="password123",
        first_name="Regular",
        last_name="User",
        phone_number="123456789",
    )


@pytest.fixture
def other_user(db):
    return User.objects.create_user(
        email="other@example.com",
        password="password123",
        first_name="Other",
        last_name="User",
        phone_number="987654321",
    )


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        email="admin@example.com",
        password="password123",
        first_name="Admin",
        last_name="User",
        phone_number="111111111",
    )


@pytest.fixture
def auth_client(user):
    client = APIClient()
    token, _ = Token.objects.get_or_create(user=user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return client


@pytest.fixture
def admin_client(admin_user):
    client = APIClient()
    token, _ = Token.objects.get_or_create(user=admin_user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return client


@pytest.fixture
def product(db):
    return Product.objects.create(
        name="Tomato",
        category="Vegetables",
        description="Fresh tomato",
    )


@pytest.fixture
def other_product(db):
    return Product.objects.create(
        name="Potato",
        category="Vegetables",
        description="Fresh potato",
    )


@pytest.fixture
def cart_item(user, product):
    return Cart.objects.create(user=user, product=product, quantity=2)


@pytest.fixture
def other_cart_item(other_user, other_product):
    return Cart.objects.create(user=other_user, product=other_product, quantity=1)


@pytest.fixture
def order(user):
    return Order.objects.create(user=user, address="Main street 1")


@pytest.fixture
def other_order(other_user):
    return Order.objects.create(user=other_user, address="Second street 2")


@pytest.fixture
def order_item(order, product):
    return OrderItem.objects.create(order=order, product=product, quantity=3)


@pytest.fixture
def other_order_item(other_order, other_product):
    return OrderItem.objects.create(order=other_order, product=other_product, quantity=4)


@pytest.fixture
def blog(user):
    return Blog.objects.create(user=user, name="First blog", content="Hello")


@pytest.fixture
def other_blog(other_user):
    return Blog.objects.create(user=other_user, name="Second blog", content="World")