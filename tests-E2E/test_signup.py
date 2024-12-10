import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client


@pytest.mark.django_db
def test_signup_page_get():
    """
    Test que la page signup est rendue correctement avec un formulaire vide.
    """
    client = Client()
    response = client.get(reverse('signup'))
    assert response.status_code == 200
    assert 'form' in response.context

@pytest.mark.django_db
def test_signup_page_post_invalid_data():
    """
    Test que le formulaire renvoie des erreurs avec des données invalides.
    """
    client = Client()
    data = {
        'username': 'testuser',
        'email': 'invalid-email',  # Email invalide
        'first_name': 'Test',
        'last_name': 'User',
        'role': 'CREATOR',
        'password1': 'testpassword123',
        'password2': 'differentpassword',  # Mots de passe différents
    }
    response = client.post(reverse('signup'), data)

    # Vérifier que le formulaire est renvoyé avec des erreurs
    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['form'].errors

@pytest.mark.django_db
def test_signup_page_post_valid_data():
    """
    Test que l'inscription fonctionne correctement avec des données valides.
    """
    client = Client()
    data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'first_name': 'Test',
        'last_name': 'User',
        'role': 'CREATOR',  # ou 'SUBSCRIBER' selon l'option
        'password1': 'testpassword123',
        'password2': 'testpassword123',
    }
    response = client.post(reverse('signup'), data)

    # Vérifier la redirection après une inscription réussie
    assert response.status_code == 302
    # Assurer la redirection vers /home/ après l'inscription
    assert response.url == '/home/'

    # Vérifier que l'utilisateur est créé
    User = get_user_model()
    user = User.objects.get(username='testuser')
    assert user.email == 'testuser@example.com'
    assert user.first_name == 'Test'
    assert user.last_name == 'User'
    assert user.role == 'CREATOR'
    assert user.check_password('testpassword123')


@pytest.mark.django_db
def test_signup_page_auto_login():
    """
    Test que l'utilisateur est automatiquement connecté après l'inscription.
    """
    client = Client()
    data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'first_name': 'Test',
        'last_name': 'User',
        'role': 'CREATOR',
        'password1': 'testpassword123',
        'password2': 'testpassword123',
    }
    response = client.post(reverse('signup'), data)

    # Vérifier la redirection après une inscription réussie
    assert response.status_code == 302
    # Assurer la redirection vers /home/ après l'inscription
    assert response.url == '/home/'

    # Vérifier que l'utilisateur est connecté
    user = get_user_model().objects.get(username='testuser')
    assert user.is_authenticated

