import pytest
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

