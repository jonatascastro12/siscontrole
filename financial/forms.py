from decimal import Decimal, DecimalException
from django.core.exceptions import ValidationError
from django.forms.fields import DecimalField
from django.forms.models import ModelForm
from django.utils.safestring import mark_safe
from input_mask.contrib.localflavor.br.fields import BRDecimalField
from input_mask.contrib.localflavor.br.widgets import BRDecimalInput
from input_mask.widgets import DecimalInputMask
from financial.models import FiCurrentAccount

class BRDecimalInput(DecimalInputMask):
    thousands_sep = '.'
    decimal_sep = ','

    def render(self, name, value, attrs=None):
        input = super(BRDecimalInput, self).render(name, value, attrs)
        input = mark_safe('<div class="input-group"><span class="input-group-addon">R$</span>' + input + '</div>');
        return input

class BRDecimalField(DecimalField):
    widget = BRDecimalInput

    def to_python(self, value):
        value = value.replace(',', '.')
        value = value.replace('.', '', value.count('.') - 1)

        try:
            value = Decimal(value)
            return value
        except DecimalException:
            raise ValidationError(self.error_messages['invalid'])

class FiCurrentAccountForm(ModelForm):
    balance = BRDecimalField()

    class Meta:
        model = FiCurrentAccount