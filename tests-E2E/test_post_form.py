import re
import os
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = '1'
from playwright.sync_api import Page, expect


def test_publish_button_is_visible(page: Page, test_server, test_user, live_server):
    page.get_by_label("Nom d’utilisateur").fill(test_user.username)
    page.get_by_label("Mot de passe").fill("secure_password")
    page.get_by_role("button", name="Se connecter").click()
    page.goto(live_server.url+"/blog/create")

    publish_button = page.get_by_test_id("publish_button")
    expect(publish_button).to_be_visible()


def test_post_form_is_visible(page: Page, test_server, test_user, live_server):
    page.get_by_label("Nom d’utilisateur").fill(test_user.username)
    page.get_by_label("Mot de passe").fill("secure_password")
    page.get_by_role("button", name="Se connecter").click()
    page.goto(live_server.url+"/blog/create")
    post_form = page.get_by_test_id("post_form")
    expect(post_form).to_be_visible()

# def test_connection_works_and_redirects_home(page: Page, test_user, live_server, test_server):
#     page.get_by_label("Nom d’utilisateur").fill(test_user.username)
#     page.get_by_label("Mot de passe").fill("secure_password")
#     page.get_by_role("button", name="Se connecter").click()
#
#     assert page.url == live_server.url + "/home/"
