import os
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = '1'
from playwright.sync_api import Page, expect

class TestPostForm:

    def _login(self, page: Page, test_user):
        page.get_by_label("Nom d’utilisateur").fill(test_user.username)
        page.get_by_label("Mot de passe").fill("secure_password")
        page.get_by_role("button", name="Se connecter").click()

    def test_publish_button_is_visible(self, page: Page, test_server, test_user, live_server):
        self._login(page, test_user)
        page.goto(live_server.url + "/blog/create")
        publish_button = page.get_by_test_id("publish_button")
        expect(publish_button).to_be_visible()

    def test_post_form_is_visible(self, page: Page, test_server, test_user, live_server):
        self._login(page, test_user)
        page.goto(live_server.url+"/blog/create")
        post_form = page.get_by_test_id("post_form")
        expect(post_form).to_be_visible()


    def test_title_input_is_visible(self, page: Page, test_server, test_user, live_server):
        self._login(page, test_user)
        page.goto(live_server.url+"/blog/create")
        title_input = page.locator("#id_title")
        # title_input = page.query_selector("#id_title")
        expect(title_input).to_be_visible()

    def test_content_input_is_visible(self, page: Page, test_server, test_user, live_server):
        self._login(page, test_user)
        page.goto(live_server.url+"/blog/create")
        content_input = page.locator("#id_content")
        expect(content_input).to_be_visible()

    def test_image_input_is_visible(self, page: Page, test_server, test_user, live_server):
        self._login(page, test_user)
        page.goto(live_server.url+"/blog/create")
        image_input = page.locator("#id_image")
        expect(image_input).to_be_visible()

    def test_caption_input_is_visible(self, page: Page, test_server, test_user, live_server):
        self._login(page, test_user)
        page.goto(live_server.url+"/blog/create")
        caption_input = page.locator("#id_caption")
        expect(caption_input).to_be_visible()

    def test_publishing_works_and_redirects_home(self, page: Page, test_user, live_server, test_server):
        self._login(page, test_user)
        page.goto(live_server.url+"/blog/create")
        page.get_by_label("Title").fill("test")
        page.get_by_label("Content").fill("test")
        page.get_by_label("Caption").fill("test")
        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../media/avatar.jpg"))
        page.locator("#id_image").set_input_files(image_path)
        page.get_by_role("button", name="Publier").click()
        assert page.url == live_server.url + "/home/"
