from decimal import Decimal, DecimalException
from bootstrap3_datetime.widgets import DateTimePicker
from django.core.exceptions import ValidationError
from django.db.models.query_utils import Q
from django.forms.fields import DecimalField, CharField
from django.forms.models import ModelForm, inlineformset_factory, ModelChoiceField
from django.forms.widgets import DateInput
from django.utils import numberformat
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django_select2.fields import AutoModelSelect2Field, ModelSelect2Field
from django_select2.views import NO_ERR_RESP
from input_mask.contrib.localflavor.br.fields import BRDecimalField
from input_mask.contrib.localflavor.br.widgets import BRDecimalInput
from input_mask.utils import chunks
from input_mask.widgets import DecimalInputMask, InputMask
from financial.models import FiCurrentAccount, FiCostCenter, FiAccountGroup, FiAccount, FiSubaccount, FiSubaccountType, \
    FiEntry, FiWriteOff
from siscontrole.forms import ExtendedAutoHeavySelectWidget, Select2Widget


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


class FiGenericChoices(AutoModelSelect2Field):
    queryset = None
    widget = ExtendedAutoHeavySelectWidget

    def get_results(self, request, term, page, context):
        try:
            term = unicode(int(term))
        except ValueError:
            term = unicode(term)
        objects = self.queryset.filter((Q(id__icontains=term) | Q(name__icontains=term)))
        res = [(obj.id, "%s - %s" % (obj.get_code(), obj.name),) for obj in objects]
        return (NO_ERR_RESP, False, res, ) # Any error response, Has more results, options list


class FiAccountGroupChoices(FiGenericChoices):
    queryset = FiAccountGroup.objects.all()

class FiAccountChoices(FiGenericChoices):
    queryset = FiAccount.objects.all()

class FiSubaccountChoices(FiGenericChoices):
    queryset = FiSubaccount.objects.all()

class FiSubaccountTypeChoices(FiGenericChoices):
    queryset = FiSubaccountType.objects.all()

class FiEntryForm(ModelForm):

    class Meta:
        model = FiEntry
        widgets = {
            'date': DateTimePicker(options={"format": "DD/MM/YYYY", "pickTime": False}),
            'expiration_date': DateTimePicker(options={"format": "DD/MM/YYYY", "pickTime": False}),
            'document_type': Select2Widget,
            'department': Select2Widget,
            'client_supplier': Select2Widget,
            'value': DecimalInputMask,

        }


class FiCostCenterForm(ModelForm):
    class Meta:
        model = FiCostCenter
        widgets = {
            'account_group': Select2Widget,
            'account': Select2Widget,
            'subaccount': Select2Widget,
            'subaccount_type': Select2Widget,
        }

class FiWriteOffForm(ModelForm):
    class Model:
        model = FiWriteOff


FiWriteOffFormset = inlineformset_factory(FiEntry, FiWriteOff, min_num=1, extra=0, form=FiWriteOffForm, widgets={
})