from django.core.validators import RegexValidator
import re

def validate_mobile_number(number):
    """
    Validator to check that the mobile number is valid (matches a given pattern).
    Example: Allows optional + and country code, with 9 to 15 digits.
    """
    pattern = r'^\+?1?\d{9,15}$'
    if not re.match(pattern, number):
        raise ValidationError('Enter a valid phone number.')
