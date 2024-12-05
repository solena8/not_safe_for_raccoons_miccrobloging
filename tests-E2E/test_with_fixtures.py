import pytest
import os
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = '1'
from playwright.sync_api import Page
import threading
from authentication.models import User


base_url = "http://127.0.0.1:8000/"


def create_test_user():
    return User.objects.create_user(
        username="test_user",
        password="secure_password"
    )


@pytest.fixture
def test_user(db):
    user_thread = threading.Thread(target=create_test_user)
    user_thread.start()
    user_thread.join()

    return {
        "username": "test_user",
        "password": "secure_password"
    }


def test_login(page: Page, test_user):
    page.goto(base_url)
    page.get_by_label("Nom d’utilisateur").fill(test_user["username"])
    page.get_by_label("Mot de passe").fill(test_user["password"])
    page.get_by_role("button", name="Se connecter").click()
    assert page.url == "http://127.0.0.1:8000/home/"
