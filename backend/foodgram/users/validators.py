import re

from django.core.exceptions import ValidationError


def validate_name(value):
    if len(value) < 3:
        raise ValidationError(
            'login должен содержать минимум три символа.'
        )
    elif not re.match(r'^[\w.@+-]+\Z', value):
        raise ValidationError(
            '''Используйте здесь латинские буквы,
            цифры и символы(@_-=.) без пробелов.'''
        )
    return value
