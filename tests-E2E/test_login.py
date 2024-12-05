import re
import os
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = '1'
from playwright.sync_api import Page, expect


def test_has_title(page: Page, test_server):
    expect(page).to_have_title(re.compile("Not Safe For Raccoons"))


def test_connect_button_is_visible(page: Page, test_server):
    login_button = page.get_by_test_id("login_button")
    expect(login_button).to_be_visible()


def test_connect_username_form_is_visible(page: Page, test_server):
    login_form = page.get_by_test_id("login_form")
    expect(login_form).to_be_visible()

def test_connection_works_and_redirects_home(page: Page, test_user, live_server, test_server):
    page.get_by_label("Nom d’utilisateur").fill(test_user.username)
    page.get_by_label("Mot de passe").fill("secure_password")
    page.get_by_role("button", name="Se connecter").click()

    assert page.url == live_server.url + "/home/"
