import os
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = '1'
from playwright.sync_api import Page
from django.conf import settings

# @todo spliter le test en 3 testsgit pull
# @todo classes et éviter la répétition de code ?

class TestSession:

    def _login(self, page: Page, test_user):
        page.get_by_label("Nom d’utilisateur").fill(test_user.username)
        page.get_by_label("Mot de passe").fill("secure_password")
        page.get_by_role("button", name="Se connecter").click()

    def test_session_persists(self,page: Page, test_user, test_server, live_server):
        # 1. Connecte l'utilisateur
        self._login(page, test_user)

        # 2. Récupère le cookie de session après connexion
        cookies = page.context.cookies()

        session_cookie =None
        for cookie in cookies :
            if cookie["name"] == settings.SESSION_COOKIE_NAME:
                session_cookie = cookie
                break

        # session_cookie = next(
        #     (cookie for cookie in cookies if cookie["name"] == settings.SESSION_COOKIE_NAME),
        #     None
        # )

        assert session_cookie is not None, "Le cookie de session n'a pas été trouvé après la connexion"
        # 3. Navigue vers une autre page et vérifie si la session est toujours active
        page.goto(live_server.url)
        cookies_after_navigation = page.context.cookies()

        session_cookie_after_navigation = None
        for cookie in cookies_after_navigation:
            if cookie["name"] == settings.SESSION_COOKIE_NAME:
                session_cookie_after_navigation = cookie
                break

        assert session_cookie_after_navigation is not None, "Le cookie de session a disparu après navigation"
        assert session_cookie["value"] == session_cookie_after_navigation["value"], "La session n'a pas persisté"
