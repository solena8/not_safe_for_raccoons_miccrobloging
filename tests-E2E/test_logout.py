import os
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = '1'

import os
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = '1'
from playwright.sync_api import Page
from django.conf import settings

class TestLogout:

    def _login(self, page: Page, test_user):
        page.get_by_label("Nom d’utilisateur").fill(test_user.username)
        page.get_by_label("Mot de passe").fill("secure_password")
        page.get_by_role("button", name="Se connecter").click()

    def test_logout_deletes_sessionid(self, page: Page, test_user, test_server):
        # 1. Connecte l'utilisateur
        self._login(page, test_user)
        # 2. Récupère le cookie de session après connexion
        cookies = page.context.cookies()

        session_cookie = None
        for cookie in cookies :
            if cookie["name"] == settings.SESSION_COOKIE_NAME:
                session_cookie = cookie
                break

        # 3. déconnecte et vérifie que les cookies n'ont plus de sessionid
        page.get_by_role("button", name="Se déconnecter").click()

        cookies_after_logout = page.context.cookies()

        session_cookie_after_logout = None
        for cookie in cookies_after_logout :
            if cookie["name"] == settings.SESSION_COOKIE_NAME:
                session_cookie_after_logout = cookie

        assert session_cookie_after_logout is None