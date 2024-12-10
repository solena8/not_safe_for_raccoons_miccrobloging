import pytest
from django.core.exceptions import ValidationError
from authentication.validators import ContainsLetterValidator, ContainsNumberValidator


def test_letter_validator_validate_valid_password():
    validator_letter = ContainsLetterValidator()
    password = "ValidPassword123"
    validator_letter.validate(password)
    assert True


def test_number_validator_validate_valid_password():
    validator_number = ContainsNumberValidator()
    password = "ValidPassword123"
    validator_number.validate(password)
    assert True


def test_digit_only_password_raise_validation_error():
    validator_letter = ContainsLetterValidator()
    password = "123456"
    with pytest.raises(ValidationError):
        validator_letter.validate(password)


def test_letters_only_password_raise_validation_error():
    validator_number = ContainsNumberValidator()
    password = "Password"
    with pytest.raises(ValidationError):
        validator_number.validate(password)
