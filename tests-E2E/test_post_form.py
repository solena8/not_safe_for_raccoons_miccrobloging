import os
import tempfile

# Permet d'utiliser du code asynchrone non sécurisé dans un environnement Django.
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = '1'

from playwright.sync_api import Page, expect
from django.conf import settings
from unittest.mock import patch


class TestPostForm:

    # Méthode pour connecter un utilisateur sur le formulaire de connexion.
    def _login(self, page: Page, test_user):
        page.get_by_label("Nom d’utilisateur").fill(test_user.username)  # Remplit le champ "Nom d'utilisateur".
        page.get_by_label("Mot de passe").fill("secure_password")  # Remplit le champ "Mot de passe".
        page.get_by_role("button", name="Se connecter").click()  # Clique sur le bouton "Se connecter".

    def test_publish_button_is_visible(self, page: Page, test_server, test_user, live_server):
        self._login(page, test_user)  # Connexion de l'utilisateur.
        page.goto(live_server.url + "/blog/create")  # Accède à la page de création.
        publish_button = page.get_by_test_id("publish_button")  # Sélectionne le bouton "Publier".
        expect(publish_button).to_be_visible()  # Vérifie qu'il est visible.

    # Vérifie que le formulaire d'article est visible.
    def test_post_form_is_visible(self, page: Page, test_server, test_user, live_server):
        self._login(page, test_user)
        page.goto(live_server.url + "/blog/create")
        post_form = page.get_by_test_id("post_form")  # Sélectionne le formulaire d'article.
        expect(post_form).to_be_visible()

    # Vérifie que le champ de titre est visible.
    def test_title_input_is_visible(self, page: Page, test_server, test_user, live_server):
        self._login(page, test_user)
        page.goto(live_server.url + "/blog/create")
        title_input = page.locator("#id_title")  # Localise le champ de titre.
        expect(title_input).to_be_visible() # Vérifie qu'il est visible.

    # Vérifie que le champ de contenu est visible.
    def test_content_input_is_visible(self, page: Page, test_server, test_user, live_server):
        self._login(page, test_user)
        page.goto(live_server.url + "/blog/create")
        content_input = page.locator("#id_content")  # Localise le champ de contenu.
        expect(content_input).to_be_visible()

    # Vérifie que le champ d'image est visible.
    def test_image_input_is_visible(self, page: Page, test_server, test_user, live_server):
        self._login(page, test_user)
        page.goto(live_server.url + "/blog/create")
        image_input = page.locator("#id_image")  # Localise le champ d'image.
        expect(image_input).to_be_visible()

    # Vérifie que le champ de légende (caption) est visible.
    def test_caption_input_is_visible(self, page: Page, test_server, test_user, live_server):
        self._login(page, test_user)
        page.goto(live_server.url + "/blog/create")
        caption_input = page.locator("#id_caption")  # Localise le champ de légende.
        expect(caption_input).to_be_visible()

    # Vérifie que la publication d'un article fonctionne et redirige vers la page d'accueil.
    def test_publishing_works_and_redirects_home(self, page: Page, test_user, live_server, test_server):
        # Utilisation de `unittest.mock.patch` pour simuler les actions liées aux fichiers et éviter des erreurs dues au stockage réel.
        with patch.object(settings, 'MEDIA_ROOT',
                          tempfile.mkdtemp()):  # Redirige MEDIA_ROOT vers un répertoire temporaire.
            with patch('django.core.files.storage.FileSystemStorage.save', return_value='mocked_image.jpg'), \
                    patch('django.core.files.storage.FileSystemStorage.delete'), \
                    patch('os.remove'), \
                    patch('shutil.rmtree'):  # Simule les actions de sauvegarde, suppression et nettoyage des fichiers.

                self._login(page, test_user)  # Connexion de l'utilisateur.
                page.goto(live_server.url + "/blog/create")  # Accède à la page de création d'article.

                # Remplit les champs du formulaire.
                page.get_by_label("Title").fill("test")
                page.get_by_label("Content").fill("test")
                page.get_by_label("Caption").fill("test")

                # Charge une image test dans le champ d'image.
                image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../media/avatar.jpg"))
                page.locator("#id_image").set_input_files(image_path)

                # Clique sur le bouton "Publier".
                page.get_by_role("button", name="Publier").click()

                # Vérifie que l'utilisateur est redirigé vers la page d'accueil après la publication.
                assert page.url == live_server.url + "/home/"
