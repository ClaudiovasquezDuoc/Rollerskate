import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class ValidarContrasenaSegura:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(_("La contraseña debe tener al menos 8 caracteres."))
        if not re.search(r'[A-Za-z]', password):
            raise ValidationError(_("La contraseña debe contener al menos una letra."))
        if not re.search(r'\d', password):
            raise ValidationError(_("La contraseña debe contener al menos un número."))
        if not re.search(r'[^\w\s]', password):
            raise ValidationError(_("La contraseña debe contener al menos un símbolo especial."))

    def get_help_text(self):
        return _("Tu contraseña debe tener al menos 8 caracteres, una letra, un número y un símbolo.")