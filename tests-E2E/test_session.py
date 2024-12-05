import os
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = '1'
from playwright.sync_api import Page

#
#
# def test_session_persists(page: Page, test_user, live_server, test_server):
#     page.get_by_label("Nom d’utilisateur").fill(test_user.username)
#     page.get_by_label("Mot de passe").fill("secure_password")
#     page.get_by_role("button", name="Se connecter").click()
#     page.goto(live_server.url)
#     session_storage = page.evaluate("() => JSON.stringify(sessionStorage)")
#     assert "key_associated_with_session" in session_storage
#
