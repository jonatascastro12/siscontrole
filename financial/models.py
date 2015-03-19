from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.
from django.db.models import permalink
from django.db.models.base import Model
from django.utils.translation import ugettext as _, pgettext as p_
from simple_history.models import HistoricalRecords
from main.models import MaDepartment, MaCustomerSupplier, MaBank, MaBankAccount, MaPerson


class FiDocumentType(Model):
    name = models.CharField(max_length=255, verbose_name=_('Document type name'))
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Description'))

    def __unicode__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        return ('financial_documenttype_edit', (), {'pk': self.id})

    class Meta:
        verbose_name = _('Document Type')
        verbose_name_plural = _('Document Types')

class FiAccountGroup(Model):
    name = models.CharField(max_length=100, verbose_name=_('Account group name'))

    def __unicode__(self):
        return str(self.id) + ' - ' + self.name

    def get_code(self):
        return str(self.id).zfill(4)

    @permalink
    def get_absolute_url(self):
        return ('financial_accountgroup_edit', (), {'pk': self.id})

    class Meta:
        verbose_name = _('Account Group')

class FiAccount(Model):
    name = models.CharField(max_length=100, verbose_name=_('Account name'))
    type = models.CharField(max_length=100, choices=(('E', _('Expense')), ('R', _('Revenue')),), verbose_name=_('Account type'))

    def __unicode__(self):
        return str(self.id) + ' - ' + self.name

    def get_code(self):
        return str(self.id).zfill(4)

    def get_type_icon(self):
        if self.type == 'E':
            return '<span class="fa fa-level-down text-danger" title="' + _('Expense') + '"></span> <span class="text-danger">'+_('Expense')+'</span>'
        else:
            return '<span class="fa fa-level-up text-success" title="' + _('Revenue') + '"></span> <span class="text-success">'+_('Revenue')+'</span>'

    @permalink
    def get_absolute_url(self):
        return ('financial_account_edit', (), {'pk': self.id})

    class Meta:
        verbose_name = _('Account')
        gender = 'F'


class FiSubaccount(Model):
    name = models.CharField(max_length=100, verbose_name=_('Subaccount name'))

    def __unicode__(self):
        return str(self.id) + ' - ' + self.name

    def get_code(self):
        return str(self.id).zfill(4)

    @permalink
    def get_absolute_url(self):
        return ('financial_subaccount_edit', (), {'pk': self.id})

    class Meta:
        verbose_name = _('Subaccount')
        gender = 'F'

class FiSubaccountType(Model):
    name = models.CharField(max_length=100, verbose_name=_('Subaccount type name'))
    subaccount = models.ForeignKey(FiSubaccount, verbose_name=_('Subaccount'))
    nature = models.CharField(max_length=2, choices=(('O', _('Operational')), ('OO', _('One-off')), ('I', _('Indirect')), ), verbose_name=_('Subaccount type nature'))

    def __unicode__(self):
        return str(self.id) + ' - ' + self.name

    def get_code(self):
        return str(self.id).zfill(4)

    @permalink
    def get_absolute_url(self):
        return ('financial_subaccounttype_edit', (), {'pk': self.id})

    class Meta:
        verbose_name = _('Subaccount Type')

class FiCostCenter(Model):
    account_group = models.ForeignKey(FiAccountGroup, verbose_name=_('Account group'))
    account = models.ForeignKey(FiAccount, verbose_name=_('Account'))
    subaccount = models.ForeignKey(FiSubaccount, verbose_name=_('Subaccount'))
    subaccount_type = models.ForeignKey(FiSubaccountType, verbose_name=_('Subaccount type'))

    def __unicode__(self):
        return self.get_code()

    def get_code(self):
        return "%s.%s.%s.%s" % (self.account_group.get_code(), self.account.get_code(), self.subaccount.get_code(), self.subaccount_type.get_code())

    @permalink
    def get_absolute_url(self):
        return ('financial_costcenter_detail', (), {'pk': self.id})

    class Meta:
        verbose_name = _('Cost Center')
        verbose_name_plural = _('Cost Centers')
        unique_together = ('account_group', 'account', 'subaccount', 'subaccount_type')

class FiCurrentAccount(Model):
    name = models.CharField(max_length=100, verbose_name=_('Account name'))
    bank = models.ForeignKey(MaBank, verbose_name=_('Bank'))
    agency = models.CharField(max_length=20, verbose_name=_('Agency'))
    number = models.CharField(max_length=20, verbose_name=_('Account number'))
    related_account = models.ForeignKey(MaBankAccount, null=True, blank=True)

    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('Balance'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Current account")
        verbose_name_plural = _("Current accounts")
        gender = 'F'

    @permalink
    def get_absolute_url(self):
        return ('financial_currentaccount_edit', (), {'pk': self.id})

class FiEntry(Model):
    date = models.DateField(verbose_name=_("Date"))
    costcenter = models.ForeignKey(FiCostCenter, verbose_name=_("Cost Center"))
    current_account = models.ForeignKey(FiCurrentAccount, verbose_name=_('Current Account'))
    document_type = models.ForeignKey(FiDocumentType, verbose_name=_('Document Type'))
    document_number = models.CharField(max_length=100, verbose_name=_('Document Number'))
    cheque_number = models.CharField(max_length=100, blank=True, null=True)
    expiration_date = models.DateField(verbose_name=_('Expiration Date'))
    department = models.ForeignKey(MaDepartment, verbose_name=_('Department'))
    client_supplier = models.ForeignKey(MaCustomerSupplier, verbose_name=_('Client/Supplier'))
    record = models.CharField(max_length=255, blank=True, null=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=1, choices=(('1', 'ONE'), ('2', 'TWO')))
    status = models.CharField(max_length=2, choices=(('R', _('Receivable')), ('P', _('Payable')), ('RR', _('Received')),
                                                     ('PP', _('Paid'))))

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Entry')

class FiWriteOff(Model):
    date = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    third_party = models.CharField(max_length=100, blank=True, null=True)
    third_party_bank = models.ForeignKey(MaBank, blank=True, null=True)
    third_party_agency = models.CharField(max_length=30, blank=True, null=True)
    entry = models.ForeignKey(FiEntry, null=True)

    class Meta:
        verbose_name = _('Write off')
        gender = 'F'
