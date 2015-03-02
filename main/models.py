from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.
from django.db.models import permalink
from django.db.models.base import Model
from django.utils.translation import ugettext as _
from django_localflavor_br.br_states import STATE_CHOICES


class MaDepartment(Model):
    name = models.CharField(max_length=255, verbose_name=_("Department Name"))

    def __unicode__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        return ('main_department_edit', (), {'pk': self.id})

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
    name = models.CharField(max_length=255)
    fantasy_name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)

    person_type = models.CharField(max_length=10, choices=(('N', 'Natural'),('L', 'Legal')))
    cpf = models.CharField(max_length=14)
    rg = models.CharField(max_length=14)
    cnpj = models.CharField(max_length=18)
    state_registration = models.CharField(max_length=11)

    email = models.EmailField(blank=True, null=True)
    site = models.URLField(blank=True, null=True)
    phone1 = models.CharField(max_length=20, blank=True, null=True)
    phone2 = models.CharField(max_length=20, blank=True, null=True)

    address = models.CharField(max_length=255, blank=True, null=True)
    address_number = models.CharField(max_length=15, blank=True, null=True)
    address_complement = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True, choices=STATE_CHOICES)
    zipcode = models.CharField(max_length=255, blank=True, null=True)
    neighborhood = models.CharField(max_length=255, blank=True, null=True)

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class MaEmployeeFunction(Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)

class MaEmployee(MaPerson):
    function = models.ForeignKey(MaEmployeeFunction)
    department = models.ForeignKey(MaDepartment)

class MaBank(Model):
    number = models.PositiveIntegerField()
    name = models.CharField(max_length=255)

class MaBankAccount(Model):
    bank = models.ForeignKey(MaBank)
    number = models.PositiveIntegerField()
    

class MaCustomerSupplier(MaPerson):
    type = models.CharField(max_length=10, choices=(('C', 'Customer'), ('S', 'Supplier'),
                                                    ('C/S', 'Customer and Supplier')))
    bank_accounts = models.ManyToManyField(MaBankAccount)

