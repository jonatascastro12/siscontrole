# -*- coding: utf-8 -*-

from decimal import Decimal, DecimalException
from django.core.exceptions import ValidationError
from django.db.models.query_utils import Q
from django.forms.fields import DecimalField, CharField, BooleanField
from django.forms.models import ModelForm, inlineformset_factory, ModelChoiceField
from django.forms.widgets import DateInput, TextInput, ChoiceInput
from django.utils import numberformat
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django_select2.fields import AutoModelSelect2Field, ModelSelect2Field
from django_select2.views import NO_ERR_RESP
from django_select2.widgets import AutoHeavySelect2Widget
from input_mask.contrib.localflavor.br.fields import BRDecimalField
from input_mask.contrib.localflavor.br.widgets import BRDecimalInput
from input_mask.utils import chunks
from input_mask.widgets import DecimalInputMask, InputMask
from financial.models import FiCurrentAccount, FiCostCenter, FiAccountGroup, FiAccount, FiSubaccount, FiSubaccountType, \
    FiEntry, FiWriteOff, FiCheque
from main.models import MaBank, MaCustomerSupplier, MaPerson
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


def search_mask_cpf_cnpj(term):
    try:
        term = unicode(int(term))
        if len(term) < 3:
            cnpj = "%s" % term
        elif len(term) < 6:
            cnpj = "%s.%s" % (term[0:2], term[2:])
        elif len(term) < 9:
            cnpj = "%s.%s.%s" % (term[0:2], term[2:5], term[5:])
        elif len(term) < 13:
            cnpj = "%s.%s.%s/%s" % (term[0:2], term[2:5], term[5:8], term[8:])
        else:
            cnpj = "%s.%s.%s/%s-%s" % (term[0:2], term[2:5], term[5:8], term[8:12], term[12:14])

        if len(term) < 4:
            cpf = "%s" % term
        elif len(term) < 7:
            cpf = "%s.%s" % (term[0:3], term[3:])
        elif len(term) < 10:
            cpf = "%s.%s.%s" % (term[0:3], term[3:6], term[6:])
        else:
            cpf = ("%s.%s.%s-%s" % (term[0:3], term[3:6], term[6:9], term[9:]))
    except ValueError:
        term = unicode(term)
        cpf = term
        cnpj = term

    return (term, cpf, cnpj)

class MaClientSupplierChoices(AutoModelSelect2Field):
    queryset = MaCustomerSupplier.objects.all()

    def get_results(self, request, term, page, context):
        if term != '':
            terms = search_mask_cpf_cnpj(term)
            objects = self.queryset.filter((Q(person__cpf__icontains=terms[1]) | Q(person__cnpj__icontains=terms[2]) | Q(person__name__icontains=term[0]))).order_by('person__name')
        else:
            objects = self.queryset.order_by('?')[:20]
        res = [(obj.id, "%s - %s" % (obj.get_name(), obj.get_document_number())) for obj in objects]
        return (NO_ERR_RESP, False, res, ) # Any error response, Has more results, options list

class MaPersonChoices(AutoModelSelect2Field):
    queryset = MaPerson.objects.all()

    def get_results(self, request, term, page, context):
        terms = search_mask_cpf_cnpj(term)

        objects = self.queryset.filter((Q(cpf__icontains=terms[1]) | Q(cnpj__icontains=terms[2]) | Q(name__icontains=term[0]))).order_by('name')
        res = [(obj.id, "%s - %s" % (obj.name, obj.get_document_number())) for obj in objects]
        return (NO_ERR_RESP, False, res, ) # Any error response, Has more results, options list

class MaChequeChoices(AutoModelSelect2Field):
    queryset = FiCheque.objects.all()
    widget = ExtendedAutoHeavySelectWidget

    def get_results(self, request, term, page, context):
        objects = self.queryset.filter((Q(cheque_number__icontains=term))).order_by('cheque_number')
        res = [(obj.id, "%s (%s)" % (obj.id, obj.cheque_number)) for obj in objects]
        return (NO_ERR_RESP, False, res, ) # Any error response, Has more results, options list



class FiEntryForm(ModelForm):
    customer_supplier = MaClientSupplierChoices()
    value = BRDecimalField(required=True, label=_('Value'))
    cheque = MaChequeChoices(required=False, label=_('Cheque'))
    interest = BRDecimalField(required=True, label=_('Interest'))

    class Meta:
        model = FiEntry
        widgets = {
            'date': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'expiration_date': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'department': Select2Widget,
            'value': BRDecimalInput,
            'current_account': Select2Widget,
        }


class FiCostCenterForm(ModelForm):
    def clean(self):
        """
        Given the four elements of Cost Center, verify if it exists
        :return:
        """
        if len(self.cleaned_data) == 4:
            account = self.cleaned_data.get('account', None)
            account_group = self.cleaned_data.get('account_group', None)
            subaccount = self.cleaned_data.get('subaccount', None)
            subaccount_type = self.cleaned_data.get('subaccount_type', None)
            if not FiCostCenter.objects.filter(account=account, account_group=account_group, subaccount=subaccount, subaccount_type=subaccount_type).exists():
                raise ValidationError(message=_('This CC doesn\'t exist.'))

    class Meta:
        model = FiCostCenter
        widgets = {
            'account_group': Select2Widget,
            'account': Select2Widget,
            'subaccount': Select2Widget,
            'subaccount_type': Select2Widget,
        }

class FiWriteOffForm(ModelForm):
    is_cheque = BooleanField(required=False, label=_('Is Cheque?'))
    cheque_number = CharField(required=False, label=_('Number'))
    cheque_name = CharField(required=False, label=_('Name'))
    cheque_bank = ModelChoiceField(queryset=MaBank.objects, required=False, label=_('Bank'), empty_label=_('Select a bank'))
    cheque_agency = CharField(required=False, label=_('Agency'))
    value = BRDecimalField(required=True, label=_('Value'))

    def __init__(self, *args, **kwargs):
        super(FiWriteOffForm, self).__init__(*args, **kwargs)
        if self.instance.cheque is not None:
            self.fields['is_cheque'].initial = True
            self.fields['cheque_number'].initial = self.instance.cheque.cheque_number
            self.fields['cheque_name'].initial = self.instance.cheque.cheque_name
            self.fields['cheque_bank'].initial = self.instance.cheque.cheque_bank
            self.fields['cheque_agency'].initial = self.instance.cheque.cheque_agency

    def clean(self):
        super(FiWriteOffForm, self).clean()
        if self.cleaned_data.get('date', None) is None or self.cleaned_data.get('value', 0) == 0:
            raise ValidationError(_('Value can\'t be zero.'))

        is_cheque = self.cleaned_data.get('is_cheque', False)
        if is_cheque:
            cheque_number = self.cleaned_data.get('cheque_number', False)
            cheque_name = self.cleaned_data.get('cheque_name', False)
            cheque_bank = self.cleaned_data.get('cheque_bank', False)
            cheque_agency = self.cleaned_data.get('cheque_agency', False)

            if not (cheque_number and cheque_agency and cheque_bank and cheque_name):
                raise ValidationError(message=_('Complete cheque information properly.'))

    def save(self, commit=False):
        instance = super(FiWriteOffForm, self).save(commit)

        if instance.cheque is None and self.cleaned_data.get('is_cheque', False):
             cheque = FiCheque(cheque_number=self.cleaned_data.get('cheque_number'),
                          cheque_name=self.cleaned_data.get('cheque_name'),
                          cheque_bank=self.cleaned_data.get('cheque_bank'),
                          cheque_expiration_date=self.cleaned_data.get('date'),
                          cheque_value=self.cleaned_data.get('value'),
                          cheque_agency=self.cleaned_data.get('cheque_agency'))
             cheque.save()
             instance.cheque = cheque

        elif instance.cheque is not None:
            instance.cheque.cheque_number = self.cleaned_data.get('cheque_number')
            instance.cheque.cheque_name = self.cleaned_data.get('cheque_name')
            instance.cheque.cheque_bank = self.cleaned_data.get('cheque_bank')
            instance.cheque.cheque_agency = self.cleaned_data.get('cheque_agency')
            instance.cheque.cheque_expiration_date = self.cleaned_data.get('date')
            instance.cheque.cheque_value = self.cleaned_data.get('value')

        instance.save()
        return instance


    class Model:
        model = FiWriteOff

class FiChequeForm(ModelForm):
    cheque_person = MaPersonChoices(required=False, label=_('Person'))
    cheque_exists = BooleanField(required=False, label=_('Cheque already exists?'))

    class Meta:
        model = FiCheque
        widgets = {
            'cheque_bank': Select2Widget,
            'cheque_expiration_date': DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'placeholder': _('Date')}),
        }


FiWriteOffFormset = inlineformset_factory(FiEntry, FiWriteOff, min_num=1, extra=0, form=FiWriteOffForm, widgets={
    'date': DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'placeholder': _('Date')}),
})

'''FiDocument = generic_inlineformset_factory(FiEntry, ct_field="doc_content_type", fk_field="doc_object_id")'''

