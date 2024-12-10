import pytest
import django
from django.conf import settings
import os
import shutil


# Initialisation de Django
django.setup()


from authentication.models import User


@pytest.fixture()
def test_server(page, live_server):
    page.goto(live_server.url)
    return page


@pytest.fixture
def test_user(db):
    return User.objects.create_user(
        username="test_user",
        password="secure_password"
    )


# Fixture qui s'exécute avant chaque test pour créer un dossier `media` pour les tests
@pytest.fixture(scope="function", autouse=True)
def setup_media_for_tests():
    # Spécifie un chemin dans le répertoire de tests
    media_test_path = os.path.join(settings.BASE_DIR, 'test_media')

    # Crée le dossier `media` dans tests_e2e s'il n'existe pas déjà
    if not os.path.exists(media_test_path):
        os.makedirs(media_test_path)

    # Modifie temporairement MEDIA_ROOT pour qu'il pointe vers ce dossier
    original_media_root = settings.MEDIA_ROOT
    settings.MEDIA_ROOT = media_test_path

    # Pendant les tests, utilise le dossier temporaire
    yield  # Exécute les tests ici

    # Après le test, rétablit le MEDIA_ROOT et supprime le dossier temporaire `media`
    settings.MEDIA_ROOT = original_media_root
    if os.path.exists(media_test_path):
        shutil.rmtree(media_test_path)