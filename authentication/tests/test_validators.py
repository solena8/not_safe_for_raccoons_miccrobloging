from django.core.exceptions import ValidationError
from authentication.validators import ContainsLetterValidator, ContainsNumberValidator 

def test_both_validators():
    validator_letter = ContainsLetterValidator()
    validator_number = ContainsNumberValidator()

    # Mot de passe valide
    password = "ValidPassword123"
    try:
        validator_letter.validate(password)
        validator_number.validate(password)
    except ValidationError:
        assert False, "Aucune ValidationError ne devrait être levée pour un mot de passe valide."

    # Mot de passe invalide (sans lettre)
    password = "123456"
    try:
        validator_letter.validate(password)
        assert False, "ValidationError devrait être levée pour un mot de passe sans lettre."
    except ValidationError as e:
        # Vérifier le message d'erreur dans la liste
        assert str(e.message) == 'Le mot de passe doit contenir une lettre', \
            "Le message d'erreur est incorrect pour mot de passe sans lettre."
    
    # Mot de passe invalide (sans chiffre)
    password = "Password"
    try:
        validator_number.validate(password)
        assert False, "ValidationError devrait être levée pour un mot de passe sans chiffre."
    except ValidationError as e:
        # Vérifier le message d'erreur dans la liste
        assert str(e.message) == 'Le mot de passe doit contenir un chiffre', \
            "Le message d'erreur est incorrect pour mot de passe sans chiffre."
