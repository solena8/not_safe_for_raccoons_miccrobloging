import re
import os

os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = '1'
from playwright.sync_api import Page, expect


class TestLogin:

    def _login(self, page: Page, test_user):
        page.get_by_label("Nom d’utilisateur").fill(test_user.username)
        page.get_by_label("Mot de passe").fill("secure_password")
        page.get_by_role("button", name="Se connecter").click()

    def test_has_title(self, page: Page, test_server):
        expect(page).to_have_title(re.compile("Not Safe For Raccoons"))

    def test_connect_button_is_visible(self, page: Page, test_server):
        login_button = page.get_by_test_id("login_button")
        expect(login_button).to_be_visible()

    def test_connect_username_form_is_visible(self, page: Page, test_server):
        login_form = page.get_by_test_id("login_form")
        expect(login_form).to_be_visible()

    def test_connection_works_and_redirects_home(self, page: Page, test_user, live_server, test_server):
        self._login(page, test_user)
        assert page.url == live_server.url + "/home/"
