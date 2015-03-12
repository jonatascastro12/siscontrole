# -*- coding: utf-8 -*-
from bootstrap3_datetime.widgets import DateTimePicker
from django.conf.global_settings import STATIC_ROOT
from django.core.exceptions import ValidationError
from django.db.models.query_utils import Q
from django.forms.fields import DateField
from django.forms.models import inlineformset_factory
from django.forms.widgets import RadioSelect, RadioFieldRenderer
from django.utils.encoding import force_text
from django.utils.html import format_html_join
from django.utils.translation import ugettext as _
from django_localflavor_br.forms import BRCPFField, BRZipCodeField, BRPhoneNumberField, BRCNPJField
from django_select2.fields import Select2MultipleChoiceField, HeavySelect2ChoiceField, AutoModelSelect2Field, \
    ModelSelect2Field, HeavyModelSelect2ChoiceField, AutoModelSelect2MultipleField
from django_select2.views import NO_ERR_RESP
from django_select2.widgets import AutoHeavySelect2Widget
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

class ExtendedAutoHeavySelectWidget(AutoHeavySelect2Widget):
    class Media(AutoHeavySelect2Widget.Media):
        css = AutoHeavySelect2Widget.Media.css
        css['screen'] = css['screen'] + ('css/select2-bootstrap.css', )

class MaPersonChoices(AutoModelSelect2Field):
    queryset = MaPerson.objects.filter(Q(person_type__icontains='N'))
    widget = ExtendedAutoHeavySelectWidget

    def get_results(self, request, term, page, context):
        #Get only natural persons matching Name or CPF
        persons = MaPerson.natural_people.filter( (Q(name__icontains=term) | Q(cpf__icontains=term)) )
        res = [(person.id, "%s - %s" % (person.name, person.cpf),) for person in persons]
        return (NO_ERR_RESP, False, res, ) # Any error response, Has more results, options list



class MaMultiPersonForm(BetterModelForm):
    cpf = BRCPFField(required=False, label='CPF', widget=BRCPFInput)
    cnpj = BRCNPJField(required=False, label='CNPJ', widget=BRCNPJInput)
    zipcode = BRZipCodeField(required=False, label=_('Zipcode'), widget=BRZipCodeInput)
    phone1 = BRPhoneNumberField(required=False, label=_('Phone 1'), widget=BRPhoneNumberInput)
    phone2 = BRPhoneNumberField(required=False, label=_('Phone 2'), widget=BRPhoneNumberInput)
    birth_date = DateField(required=False, widget=DateTimePicker(options={"format": "DD/MM/YYYY",
                                       "pickTime": False}), label=_('Birth date'))
    representative = MaPersonChoices(required=False)

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
            (_('Legal Personal Information'), {'classes': ['legal-person'], 'fields': ['fantasy_name', 'cnpj', 'state_registration', 'representative']}),
            (_('Photo'), {'fields': ['photo']}),
            (_('Contact Information'), {'fields': ['email', 'phone1', 'phone2', 'address', 'address_number',
                                                         'address_complement', 'neighborhood', 'city', 'state',
                                                         'zipcode', ]}), ]

class MaCustomerSupplierForm(BetterModelForm):
    class Meta:
        model = MaCustomerSupplier
        exclude = ['bank_accounts', 'person']
        widgets = {
            'type': RadioSelect(renderer=BetterRadioFieldRenderer),
        }

MaRepresentativeFormset = inlineformset_factory(MaPerson, MaPerson, min_num=0, max_num=1, extra=1)
MaBankAccountFormset = inlineformset_factory(MaPerson, MaBankAccount, min_num=0, extra=1)