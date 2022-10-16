import re

from django.core.exceptions import ValidationError


def validate_name(value):
    if len(value) < 3:
        raise ValidationError(
            'username должен содержать минимум три символа.'
        )
    elif not re.match(r'^[\w.@+-]+\Z', value):
        raise ValidationError(
            'В username используются запрещенные символы'
        )
    return value
