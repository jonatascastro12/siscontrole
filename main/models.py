# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import models

# Create your models here.
from django.db.models import permalink
from django.db.models.base import Model
from django.utils.translation import ugettext as _
from django_localflavor_br.br_states import STATE_CHOICES
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
    name = models.CharField(max_length=100, verbose_name=_("Equipment Name"))
    description = models.CharField(max_length=255, blank=True, null=True)

class MaEquipment(Model):
    name = models.CharField(max_length=100)
    equipment_type = models.ForeignKey(MaEquipmentType)
    brand = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    registration = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

class MaPerson(Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    fantasy_name = models.CharField(max_length=255, verbose_name=_('Fantasy Name'), blank=True, null=True)
    contact_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Contact Name'))

    person_type = models.CharField(max_length=10, choices=(('N', 'Natural'), ('L', 'Legal')), verbose_name=_('Person Type'))
    cpf = models.CharField(max_length=14, blank=True, null=True, verbose_name=_('CPF'))
    rg = models.CharField(max_length=14, blank=True, null=True, verbose_name=_('RG'))
    cnpj = models.CharField(max_length=18, blank=True, null=True, verbose_name=_('CNPJ'))
    #. Translators: State Registration é Inscricao estadual
    state_registration = models.CharField(max_length=11, blank=True, null=True, verbose_name=_('State Registration'))

    photo = CropImageModelField(upload_to='person/', url='/upload_photo', blank=True, null=True, verbose_name=_('Foto'))

    birth_date = models.DateField(blank=True, null=True, verbose_name=_('Birth Date'))
    gender = models.CharField(max_length='1', verbose_name=_('Gender'), choices=[('M', _('Male')), ('F', _('Female'))])
    marital_status = models.CharField(max_length='1', blank=True, null=True, choices=[('S', _('Single')), ('D', _('Divorced')), ('M', _('Married')), ('W', _('Widow')), ])

    email = models.EmailField(blank=True, null=True, verbose_name=_('Email'))
    site = models.URLField(blank=True, null=True, verbose_name=_('Site'))
    phone1 = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Phone1'))
    phone2 = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Phone2'))

    address = models.CharField(max_length=255, blank=True, null=True)
    address_number = models.CharField(max_length=15, blank=True, null=True)
    address_complement = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True, choices=STATE_CHOICES)
    zipcode = models.CharField(max_length=255, blank=True, null=True)
    neighborhood = models.CharField(max_length=255, blank=True, null=True)

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        return 'main_person_edit', (), {'pk': self.id}

    class Meta:
        verbose_name = _("Person")
        verbose_name_plural = _("People")


class MaEmployeeFunction(Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Employee Function")
        verbose_name_plural = _("Employee Functions")

class MaEmployee(Model):
    function = models.ForeignKey(MaEmployeeFunction, verbose_name=_("Function"))
    department = models.ForeignKey(MaDepartment, verbose_name=_("Department"))
    person = models.OneToOneField(MaPerson)

    def __unicode__(self):
        return self.person.name

    @permalink
    def get_absolute_url(self):
        return 'main_employee_edit', (), {'pk': self.id}

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")


class MaBank(Model):
    number = models.PositiveIntegerField()
    name = models.CharField(max_length=255)

class MaBankAccount(Model):
    bank = models.ForeignKey(MaBank)
    number = models.PositiveIntegerField()
    

class MaCustomerSupplier(Model):
    type = models.CharField(max_length=10, choices=(('C', 'Customer'), ('S', 'Supplier'),
                                                    ('C/S', 'Customer and Supplier')))
    bank_accounts = models.ManyToManyField(MaBankAccount)
    person = models.OneToOneField(MaPerson)