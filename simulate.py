import requests
import random
import time
import os
from faker import Faker
from concurrent.futures import ThreadPoolExecutor
import threading

# Use environment variable if set, otherwise default to localhost:8001
# When running in Docker: docker compose exec django python simulate.py
# BASE_URL will use the django service name (http://django:8000/api)
BASE_URL = os.getenv("API_URL", "http://localhost:8001/api")
PRODUCT_IDS = list(range(1, 31))  # products 1-30
fake = Faker()

# Lock for thread-safe operations
lock = threading.Lock()


class SimUser:

    def __init__(self):
        self.email = fake.email()
        self.password = "testPassword123"
        self.token = None
        self.cart_products = []

    def headers(self):
        return {"Authorization": f"Token {self.token}"} if self.token else {}

    def register(self):

        url = f"{BASE_URL}/accounts/"

        data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": self.email,
            "phone_number": fake.phone_number(),
            "password": self.password
        }

        r = requests.post(url, data=data)

        if r.status_code in [200, 201]:
            self.token = r.json().get("token")

    def login(self):

        r = requests.post(
            f"{BASE_URL}/accounts/login/",
            json={
                "email": self.email,
                "password": self.password
            }
        )

        if r.status_code == 200:
            self.token = r.json()["token"]

    def browse(self):

        if random.random() < 0.5:
            requests.get(f"{BASE_URL}/products/")
        else:
            product = random.choice(PRODUCT_IDS)
            requests.get(f"{BASE_URL}/products/{product}/")

    def add_to_cart(self):

        if not self.token:
            return

        product = random.choice(PRODUCT_IDS)

        r = requests.post(
            f"{BASE_URL}/cart/",
            headers=self.headers(),
            json={
                "product": product,
                "quantity": random.randint(1, 3)
            }
        )

        if r.status_code in [200, 201]:
            self.cart_products.append(product)

    def checkout(self):

        if not self.token:
            return

        r = requests.post(
            f"{BASE_URL}/orders/",
            headers=self.headers(),
            json={"address": fake.address()}
        )

        if r.status_code not in [200, 201]:
            return

        order_id = r.json()["id"]

        products = random.sample(PRODUCT_IDS, random.randint(1, 3))

        for p in products:

            requests.post(
                f"{BASE_URL}/orders/items/",
                headers=self.headers(),
                json={
                    "order": order_id,
                    "product": p,
                    "quantity": random.randint(1, 2)
                }
            )


def choose_event():

    r = random.random()

    if r < 0.70:
        return "browse"

    elif r < 0.90:
        return "cart"

    elif r < 0.98:
        return "checkout"

    else:
        return "login"


def perform_event(user):
    """Perform a single random event for a user"""
    event = choose_event()

    if event == "browse":
        user.browse()
    elif event == "cart":
        user.add_to_cart()
    elif event == "checkout":
        user.checkout()
    elif event == "login":
        user.login()


def simulate(users_count=100, max_workers=50):

    users = []

    for _ in range(users_count):
        u = SimUser()
        u.register()
        users.append(u)

    print(f"{len(users)} users registered")
    print(f"Starting parallel simulation with {max_workers} concurrent workers...")

    # Use ThreadPoolExecutor for parallel requests
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        while True:
            # Submit multiple requests in parallel
            futures = []
            for _ in range(max_workers):
                user = random.choice(users)
                future = executor.submit(perform_event, user)
                futures.append(future)
            
            # Brief sleep to avoid overwhelming the server
            time.sleep(0.1)
            
            # Wait for all requests to complete before submitting next batch
            for future in futures:
                try:
                    future.result(timeout=5)
                except Exception:
                    pass  # Silently ignore request failures


if __name__ == "__main__":
    simulate(users_count=100, max_workers=50)