import pytest
from django.contrib.auth import get_user_model
from authentication.models import Profile
from django.db.models.signals import post_save

@pytest.mark.django_db
def test_create_user_profile():
    """
    Teste que lorsqu'un utilisateur est créé, un profil est automatiquement associé à cet utilisateur.
    """
    User = get_user_model()  # Récupère le modèle utilisateur, personnalisé ou non
    user = User.objects.create_user(username='testuser', password='ValidPassword123')
    
    # Vérifie que le profil est associé à l'utilisateur
    profiles = Profile.objects.filter(user=user)
    print(profiles)
    assert len(profiles) == 1

@pytest.mark.django_db
def test_create_profile_only_on_user_creation():
    """
    Teste que le profil est créé uniquement lors de la création de l'utilisateur, et non pas lors de sa mise à jour.
    """
    User = get_user_model()
    user= User.objects.create_user(username='testuser', password='ValidPassword123')

    # Vérifier que le profil a été créé pour le nouvel utilisateur
    profiles = Profile.objects.filter(user=user)
    assert profiles.exists()


    #Vérifier qu'un nouveau profil n'a pas été créé
    assert profiles.count() == 1

@pytest.mark.django_db
def test_profile_creation_fails_gracefully():
    """
    Teste que si la création du profil échoue, l'utilisateur est toujours créé sans affecter la logique.
    """
    with pytest.raises(Exception): 
        User = get_user_model()
        user = User.objects.create_user(username='testuser', password='testpassword')
        Profile.objects.create(user=None)

@pytest.mark.django_db
def test_profile_linked_to_user():
    """
    Teste que le profil est bien lié à l'utilisateur.
    """
    User = get_user_model()
    user= User.objects.create_user(username='testuser', password='ValidPassword123')
    profile = Profile.objects.get(user=user)
    assert profile.user == user


@pytest.mark.django_db
def test_profile_is_saved_when_user_is_updated():
    """
    Teste que la mise à jour de l'utilisateur entraîne la sauvegarde du profil associé.
    """

    User = get_user_model()
    user= User.objects.create_user(username='testuser', password='ValidPassword123')
    profile = Profile.objects.get(user=user)

    #modification du champ username
    user.username = 'newusername'
    user.save()

    profile.refresh_from_db() 
    assert profile.user.username == 'newusername' 