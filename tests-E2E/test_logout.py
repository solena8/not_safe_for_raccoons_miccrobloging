import os
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = '1'
from playwright.sync_api import Page


#cookies ! user.sessionid ???
# def test_logout(page: Page, test_user, live_server, test_server):
#     page.get_by_label("Nom d’utilisateur").fill(test_user.username)
#     page.get_by_label("Mot de passe").fill("secure_password")
#     page.get_by_role("button", name="Se connecter").click()
#     assert page.url == live_server.url + "/home/"
#     page.get_by_role("button", name="Se déconnecter").click()
#     session_storage = page.evaluate("() => JSON.stringify(sessionStorage)")
#     assert "key_associated_with_session" not in session_storage
#
#
