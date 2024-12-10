import pytest
import django
from playwright.sync_api import sync_playwright

# Initialisation de Django
django.setup()


from authentication.models import User


@pytest.fixture()
def test_server(page, live_server):
    page.goto(live_server.url)
    return page


@pytest.fixture
def test_user(db):
    return User.objects.create_user(
        username="test_user",
        password="secure_password"
    )

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()