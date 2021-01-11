from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


def validate_password(password):
    reg = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^\W_]{6,}$"
    if not re.findall(reg, password) == [password]:
        raise ValidationError(_("Enter a correct password, please!"), code='password_invalid')
    return True
