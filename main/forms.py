# -*- coding: utf-8 -*-

from bootstrap3_datetime.widgets import DateTimePicker
from django.core.exceptions import ValidationError
from django.forms.fields import DateField
from django.forms.models import inlineformset_factory
from django.forms.widgets import RadioSelect, RadioFieldRenderer
from django.utils.encoding import force_text
from django.utils.html import format_html_join
from django.utils.translation import ugettext as _
from django_localflavor_br.forms import BRCPFField, BRZipCodeField, BRPhoneNumberField, BRCNPJField
from form_utils.forms import BetterModelForm
from input_mask.contrib.localflavor.br.widgets import BRPhoneNumberInput, BRZipCodeInput, BRCPFInput, BRCNPJInput
from main.models import MaEmployee, MaPerson, MaBankAccount, MaCustomerSupplier


class MaEmployeeForm(BetterModelForm):
    class Meta:
        model = MaEmployee
        fieldsets = [(_('Employee Information'), {'fields': ['function', 'department']}),]
        
class MaPersonForm(BetterModelForm):
    cpf = BRCPFField(required=True, label='CPF', widget=BRCPFInput)
    zipcode = BRZipCodeField(required=False, label=_('Zipcode'), widget=BRZipCodeInput)
    phone1 = BRPhoneNumberField(required=False, label=_('Phone 1'), widget=BRPhoneNumberInput)
    phone2 = BRPhoneNumberField(required=False, label=_('Phone 2'), widget=BRPhoneNumberInput)
    birth_date = DateField(widget=DateTimePicker(options={"format": "DD/MM/YYYY",
                                       "pickTime": False}), label=_('Birth date'))

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf', None)
        if MaPerson.objects.filter(cpf=cpf).exclude(pk=self.instance.pk).exists():
            raise ValidationError(_('This CPF already exists.'))
        return cpf

    class Meta:
        model = MaPerson
        fieldsets = [(_('Personal Information'), {'fields': ['name', 'cpf', 'rg', 'birth_date', 'gender', 'marital_status', 'photo']}),
                     (_('Contact Information'), {'fields': ['email', 'phone1', 'phone2', 'address', 'address_number',
                                                         'address_complement', 'neighborhood', 'city', 'state',
                                                         'zipcode', ]}), ]


class BetterRadioFieldRenderer(RadioFieldRenderer):
   def render(self):
        return format_html_join(
            u'\n',
            u'{0}&nbsp;',
            [(force_text(w), ) for w in self],
        )


class MaMultiPersonForm(BetterModelForm):
    cpf = BRCPFField(required=False, label='CPF', widget=BRCPFInput)
    cnpj = BRCNPJField(required=False, label='CNPJ', widget=BRCNPJInput)
    zipcode = BRZipCodeField(required=False, label=_('Zipcode'), widget=BRZipCodeInput)
    phone1 = BRPhoneNumberField(required=False, label=_('Phone 1'), widget=BRPhoneNumberInput)
    phone2 = BRPhoneNumberField(required=False, label=_('Phone 2'), widget=BRPhoneNumberInput)
    birth_date = DateField(required=False, widget=DateTimePicker(options={"format": "DD/MM/YYYY",
                                       "pickTime": False}), label=_('Birth date'))

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf', '')
        if self.cleaned_data.get('person_type', None) == 'N':
            if cpf == '' or cpf is None:
                raise ValidationError(_('This field is required.'))
            elif MaPerson.objects.filter(cpf=cpf).exclude(pk=self.instance.pk).exists():
                raise ValidationError(_('This CPF already exists.'))
        return cpf

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj', '')
        if self.cleaned_data.get('person_type', None) == 'L':
            if cnpj == '' or cnpj is None:
                raise ValidationError(_('This field is required.'))
            elif MaPerson.objects.filter(cnpj=cnpj).exclude(pk=self.instance.pk).exists():
                raise ValidationError(_('This CNPJ already exists.'))
        return cnpj

    class Meta:
        model = MaPerson
        widgets = {
            'person_type': RadioSelect(renderer=BetterRadioFieldRenderer),
        }
        fieldsets = [
            (_(' '), {'classes': ['person-main'], 'fields': ['person_type', 'name']}),
            (_('Natural Personal Information'), {'classes': ['natural-person'], 'fields': ['cpf', 'rg', 'birth_date', 'gender', 'marital_status']}),
            (_('Legal Personal Information'), {'classes': ['legal-person'], 'fields': ['fantasy_name', 'contact_name', 'cnpj']}),
            (_('Photo'), {'fields': ['photo']}),
            (_('Contact Information'), {'fields': ['email', 'phone1', 'phone2', 'address', 'address_number',
                                                         'address_complement', 'city', 'state', 'zipcode',
                                                         'neighborhood']}),]

class MaCustomerSupplierForm(BetterModelForm):
    class Meta:
        model = MaCustomerSupplier
        exclude = ['bank_accounts', 'person']
        widgets = {
            'type': RadioSelect(renderer=BetterRadioFieldRenderer),
        }

MaBankAccountFormset = inlineformset_factory(MaCustomerSupplier, MaBankAccount, min_num=0, extra=1)