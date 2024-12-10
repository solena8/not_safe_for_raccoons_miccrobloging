from django.core.management.base import BaseCommand
from authentication.models import User, Profile

class Command(BaseCommand):
    help = 'Créer les profils pour tous les utilisateurs existants'

    def handle(self, *args, **kwargs):
        for user in User.objects.all():  # Utilisation du modèle User personnalisé
            Profile.objects.get_or_create(user=user)  # Créer le profil si non existant
        self.stdout.write(self.style.SUCCESS("Tous les profils manquants ont été créés."))
