from django.core.exceptions import ValidationError


def validate_positive(value):
    """Value must be strictly greater than zero."""
    if value <= 0:
        raise ValidationError("Value must be greater than zero.")


def validate_non_negative(value):
    """Value must be zero or greater."""
    if value < 0:
        raise ValidationError("Value cannot be negative.")
