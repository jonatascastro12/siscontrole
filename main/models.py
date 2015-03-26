# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import permalink
from django.db.models.base import Model
from django.db.models.manager import Manager
from django.utils.translation import ugettext as _
from django_localflavor_br.br_states import STATE_CHOICES
from simple_history.models import HistoricalRecords
from crop_image.forms import CropImageModelField


class MaDepartment(Model):
    name = models.CharField(max_length=255, verbose_name=_("Department Name"))

    def __unicode__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        return 'main_department_edit', (), {'pk': self.id}

    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")


class MaEquipmentType(Model):
    name = models.CharField(max_length=100, verbose_name=_("Equipment type name"))
    description = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        return 'main_equipmenttype_edit', (), {'pk': self.id}

    class Meta:
        verbose_name = _("Equipment Type")
        verbose_name_plural = _("Equipment Types")


class MaEquipment(Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    equipment_type = models.ForeignKey(MaEquipmentType, verbose_name=_('Equipment Type'))
    brand = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Brand'))
    model = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Model'))
    registration = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Registration'),
                                    help_text='Número de placa, chassi etc.')
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Description'))

    @permalink
    def get_absolute_url(self):
        return 'main_equipment_detail', (), {'pk': self.id}

    class Meta:
        verbose_name = _("Equipment")
        verbose_name_plural = _("Equipments")

    def __unicode__(self):
        return self.brand + ' ' + self.name


class NaturalPeopleManager(Manager):
    def get_queryset(self):
        return super(NaturalPeopleManager, self).get_queryset().filter(person_type='N')


class LegalPeopleManager(Manager):
    def get_queryset(self):
        return super(LegalPeopleManager, self).get_queryset().filter(person_type='L')


class MaPerson(Model):
    MARITAL_STATUS_CHOICES = [('S', _('Single')), ('D', _('Divorced')), ('M', _('Married')), ('W', _('Widow')), ]

    name = models.CharField(max_length=255, verbose_name=_('Name'))
    person_type = models.CharField(max_length=10, choices=(('N', _('Natural')), ('L', _('Legal'))),
                                   verbose_name=_('Person Type'), default=None)

    fantasy_name = models.CharField(max_length=255, verbose_name=_('Fantasy Name'), blank=True, null=True)
    representative = models.ForeignKey('self', null=True, verbose_name=_('Representative'))
    cnpj = models.CharField(max_length=18, blank=True, null=True, verbose_name=_('CNPJ'))

    cpf = models.CharField(max_length=14, blank=True, null=True, verbose_name=_('CPF'))
    rg = models.CharField(max_length=14, blank=True, null=True, verbose_name=_('RG'))

    # . Translators: State Registration é Inscricao estadual
    state_registration = models.CharField(max_length=11, blank=True, null=True, verbose_name=_('State Registration'))

    photo = CropImageModelField(upload_to='person/', url='/upload_photo', blank=True, null=True, verbose_name=_('Foto'))

    birth_date = models.DateField(blank=True, null=True, verbose_name=_('Birth Date'))
    gender = models.CharField(max_length='1', blank=True, null=True, verbose_name=_('Gender'),
                              choices=[('M', _('Male')), ('F', _('Female'))])
    marital_status = models.CharField(max_length='1', blank=True, null=True, choices=MARITAL_STATUS_CHOICES)

    email = models.EmailField(blank=True, null=True, verbose_name=_('Email'))
    site = models.URLField(blank=True, null=True, verbose_name=_('Site'))
    phone1 = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Phone1'))
    phone2 = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Phone2'))

    address = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Address'))
    address_number = models.CharField(max_length=15, blank=True, null=True, verbose_name=_('Address number'))
    address_complement = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Address complement'))
    city = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('City'))
    state = models.CharField(max_length=255, blank=True, null=True, choices=STATE_CHOICES, verbose_name=_('State'))
    zipcode = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Zipcode'))
    neighborhood = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Neighborhood'))

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    objects = Manager()
    natural_people = NaturalPeopleManager()
    legal_people = LegalPeopleManager()

    def __unicode__(self):
        return self.name

    def get_marital_status(self):
        return dict(self.MARITAL_STATUS_CHOICES).get(self.marital_status, '')

    def get_ocupation_icon(self):
        icons = ''
        if hasattr(self, 'maemployee'):
            icons += '<span class="fa fa-briefcase" title="' + _('Employee') + '"></span>'
        if hasattr(self, 'macustomersupplier'):
            icons += self.macustomersupplier.get_type_icon()
        return icons

    def get_type_icon(self):
        if self.person_type == 'N':
            return '<span class="fa fa-user" title="' + _('Natural Person') + '"></span>'
        elif self.person_type == 'L':
            return '<span class="fa fa-building" title="' + _('Legal Person') + '"></span>'
        else:
            return ''

    def get_represented(self):
        return MaPerson.legal_people.filter(representative=self).all()

    def get_document_number(self):
        if self.person_type == 'N':
            return self.cpf
        else:
            return self.cnpj

    @permalink
    def get_absolute_url(self):
        return 'main_person_detail', (), {'pk': self.id}

    class Meta:
        verbose_name = _("Person")
        verbose_name_plural = _("People")
        gender = 'F'


class MaEmployeeFunction(Model):
    name = models.CharField(max_length=100, verbose_name=_('Function Name'))
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Description'))

    history = HistoricalRecords()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Employee Function")
        verbose_name_plural = _("Employee Functions")
        gender = 'F'

    @permalink
    def get_absolute_url(self):
        return 'main_employeefunction_edit', (), {'pk': self.id}


class MaEmployee(Model):
    function = models.ForeignKey(MaEmployeeFunction, verbose_name=_("Function"), null=True, on_delete=models.SET_NULL)
    department = models.ForeignKey(MaDepartment, verbose_name=_("Department"), null=True, on_delete=models.SET_NULL)
    person = models.OneToOneField(MaPerson)

    history = HistoricalRecords()

    def __unicode__(self):
        return self.person.name

    def get_name(self):
        return self.person.name

    @permalink
    def get_absolute_url(self):
        return 'main_employee_detail', (), {'pk': self.id}

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")


class MaBank(Model):
    number = models.CharField(max_length=4, blank=True, null=True, verbose_name=_('Code'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    short_name = models.CharField(max_length=100, verbose_name=_('Short name'), blank=True, null=True)
    cnpj = models.CharField(max_length=18, blank=True, null=True, verbose_name=_('CNPJ'))
    site = models.URLField(blank=True, null=True, verbose_name=_('Site'))

    history = HistoricalRecords()


    def __unicode__(self):
        return (self.number + ' - ' + self.name)[:20] + '...'

    def get_code(self):
        if self.number != '':
            return self.number.zfill(3)
        return ''

    @permalink
    def get_absolute_url(self):
        return 'main_bank_edit', (), {'pk': self.id}

    class Meta:
        verbose_name = _("Bank")
        verbose_name_plural = _("Banks")


class MaCustomerSupplier(Model):
    type = models.CharField(max_length=10, choices=(('C', _('Customer')), ('S', _('Supplier')),
                                                    ('C/S', _('Customer and Supplier'))),
                            default=None,
                            verbose_name=_('Type'))
    person = models.OneToOneField(MaPerson)

    history = HistoricalRecords()

    def __unicode__(self):
        if self.person.person_type == 'N':
            return self.person.name + ' - CPF: ' + self.person.cpf
        else:
            return self.person.name + ' - CNPJ: ' + self.person.cnpj

    @permalink
    def get_absolute_url(self):
        return 'main_customer_supplier_detail', (), {'pk': self.id}

    def get_name(self):
        return self.person.name

    def get_document_number(self):
        return self.person.get_document_number()

    def get_type_icon(self):
        if self.type == 'C':
            return '<span class="fa fa-male text-success" title="' + _('Customer') + '"></span>'
        elif self.type == 'S':
            return '<span class="fa fa-truck text-danger" title="' + _('Supplier') + '"></span>'
        elif self.type == 'C/S':
            return '<span class="fa fa-male text-success" title="' + _(
                'Customer') + '"></span> <span class="fa fa-truck text-danger" title="' + _('Supplier') + '"></span>'
        else:
            return ''

    class Meta:

        verbose_name = _("Customer/Supplier")
        verbose_name_plural = _("Customer/Suppliers")


class MaBankAccount(Model):
    bank = models.ForeignKey(MaBank, verbose_name=_('Bank'))
    agency = models.CharField(max_length=20, verbose_name=_('Agency'))
    number = models.CharField(max_length=20, verbose_name=_('Account number'))
    person = models.ForeignKey(MaPerson, null=True)

    history = HistoricalRecords()

    def __unicode__(self):
        return (self.bank.short_name if self.bank.short_name is not None else self.bank.name[:10]) + \
               ' - ' + self.agency + ' - ' + self.number

    class Meta:
        verbose_name = _("Bank")
        verbose_name_plural = _("Banks")