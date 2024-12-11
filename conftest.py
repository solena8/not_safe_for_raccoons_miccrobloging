import pytest
import django

# Initialisation de Django. Cette commande configure le projet Django pour que
# les tests puissent interagir avec les modèles, la base de données, etc.
django.setup()

# Importation du modèle User depuis l'application "authentication".
from authentication.models import User

# Définition d'une fixture pytest pour démarrer un serveur de test avec Playwright (représenté par "page")
@pytest.fixture()
def test_server(page, live_server):
    page.goto(live_server.url)
    return page

# Définition d'une fixture pytest pour créer un utilisateur de test.
@pytest.fixture
def test_user(db):
    # Utilisation du système d'authentification de Django pour créer un utilisateur
    return User.objects.create_user(
        username="test_user",
        password="secure_password"
    )




