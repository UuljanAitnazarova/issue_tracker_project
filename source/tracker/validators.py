from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible


def validate_integers(value):
    try:
        if isinstance(int(value[0]), int):
            raise ValidationError('%(value)s should not contain any numbers.', params={'value': value})
    except ValidationError as e:
        raise e
    except ValueError:
        pass


@deconstructible
class SpecialSymbolsValidator(BaseValidator):
    message = 'Value "%(value)s" should not contain any special symbols!'
    code = 'invalid'

    def compare(self, a, b):
        for symbol in a:
            if symbol in b:
                return True
        return False




