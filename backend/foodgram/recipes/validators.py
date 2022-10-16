import re

from django.core.exceptions import ValidationError


def validate_slug(value):

    if not re.match(r'^[-a-zA-Z0-9_]+$', value):
        raise ValidationError(
            'В slug используются запрещенные символы'
        )
    return value
