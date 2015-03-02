from django.db import models

# Create your models here.
from django.db.models.base import Model
from main.models import MaDepartment, MaCustomerSupplier


class FiDocumentType(Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)

#class Dolar(Model):
#    pass

class FiBank(Model):
    number = models.PositiveIntegerField()
    name = models.CharField(max_length=255)

class FiCurrentAccount(Model):
    name = models.CharField(max_length=100)
    bank = models.ForeignKey(FiBank)
    agency = models.PositiveIntegerField()
    number = models.PositiveIntegerField()

    class Meta:
        unique_together = ('bank', 'agency', 'number')

class FiAccountGroup(Model):
    name = models.CharField(max_length=100)

class FiAccount(Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=(('E', 'Expense'), ('R', 'Revenue'),))

class FiSubaccount(Model):
    name = models.CharField(max_length=100)

class FiSubaccountType(Model):
    name = models.CharField(max_length=100)
    subaccount = models.ForeignKey(FiSubaccount)
    nature = models.CharField(max_length=2, choices=(('O', 'Operational'), ('OO', 'One-off'), ('I', 'Indirect'), ))

class FiCostCenter(Model):
    account_group = models.ForeignKey(FiAccountGroup)
    account = models.ForeignKey(FiAccount)
    subaccount = models.ForeignKey(FiSubaccount)
    subaccount_type = models.ForeignKey(FiSubaccountType)

    def get_number(self):
        '''TODO: GERAR NUMBERO DE CC  0000.0000.0000.0000'''
        pass

    class Meta:
        unique_together = ('account_group', 'account', 'subaccount', 'subaccount_type')

class FiWriteOff(Model):
    date = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    third_party = models.CharField(max_length=100, blank=True, null=True)
    third_party_bank = models.ForeignKey(FiBank, blank=True, null=True)
    third_party_agency = models.CharField(max_length=30, blank=True, null=True)

class FiEntry(Model):
    date = models.DateField()
    costcenter = models.ForeignKey(FiCostCenter)
    current_account = models.ForeignKey(FiCurrentAccount)
    document_type = models.ForeignKey(FiDocumentType)
    document_number = models.CharField(max_length=100)
    cheque_number = models.CharField(max_length=100, blank=True, null=True)
    expiration_date = models.DateField()
    department = models.ForeignKey(MaDepartment)
    client_supplier = models.ForeignKey(MaCustomerSupplier)
    record = models.CharField(max_length=255, blank=True, null=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=1, choices=(('1', 'ONE'), ('2', 'TWO')))
    status = models.CharField(max_length=2, choices=(('R', 'Receivable'), ('P', 'Payable'), ('RR', 'Received'), ('PP', 'Paid')))
    write_off = models.OneToOneField(FiWriteOff)
