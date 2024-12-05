import re
from playwright.sync_api import Page, expect

base_url = "http://127.0.0.1:8000/"


def test_has_title(page: Page):
    page.goto(base_url)

    expect(page).to_have_title(re.compile("Not Safe For Raccoons"))


def test_connect_button_is_visible(page: Page):
    page.goto(base_url)
    login_button = page.get_by_test_id("login_button")
    expect(login_button).to_be_visible()


def test_connect_username_form_is_visible(page: Page):
    page.goto(base_url)
    login_form = page.get_by_test_id("login_form")
    expect(login_form).to_be_visible()


def test_connection_works_and_redirects_home(page: Page):
    page.goto(base_url)
    username_label = page.get_by_label("Nom d’utilisateur")
    username_label.fill("test_1")
    password_label = page.get_by_label("Mot de passe")
    password_label.fill("test")
    page.get_by_role("button", name="Se connecter").click()
    assert page.url == base_url + "home/"
