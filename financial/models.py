from decimal import Decimal
from locale import currency
import locale
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.
from django.db.models import permalink
from django.db.models.base import Model
from django.db.models.manager import Manager
from django.utils.safestring import mark_safe
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

    def get_type_icon_only(self):
        if self.type == 'E':
            return '<span class="fa fa-level-down text-danger" title="' + _('Expense') + '"></span>'
        else:
            return '<span class="fa fa-level-up text-success" title="' + _('Revenue') + '"></span>'

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
        return ('financial_currentaccount_detail', (), {'pk': self.id})



ENTRY_DOC_TYPES = (
    ('I', _('Invoice')),
    ('C', _('Cheque')),
    ('R', _('Receipt')),
    ('D', _('Duplicate')),
    ('P', _('Promissory Note')),
    ('O', _('Other')),
)

class FiCheque(Model):
    cheque_person = models.ForeignKey(MaPerson, null=True, blank=True, verbose_name=_('Person'))
    cheque_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Person Name'))
    cheque_destiny = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Destiny'))
    cheque_bank = models.ForeignKey(MaBank, verbose_name=_('Bank'))
    cheque_agency = models.CharField(max_length=20, null=True, blank=True, verbose_name=_('Agency'))
    cheque_current_account = models.CharField(max_length=20, null=True, blank=True, verbose_name=_('Current account'))
    cheque_expiration_date = models.DateField(verbose_name=_('Expiration Date'))
    cheque_number = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Number'))
    cheque_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name=_('Value'))

    def __unicode__(self):
        return str(self.id)

    def get_formated_value(self):
        locale.setlocale(locale.LC_MONETARY, '')
        return locale.currency(self.cheque_value)

    def get_cheque_name(self):
        if self.cheque_person:
            return 'Person: %s' % self.cheque_person.name
        else:
            return self.cheque_name

    def get_formated_expiration_date(self):
        return self.cheque_expiration_date.strftime("%d/%m/%Y")

    @permalink
    def get_absolute_url(self):
        return ('financial_cheque_detail', (), {'pk': self.id})

    class Meta:
        verbose_name = _('Cheque')


class FiEntry(Model):
    date = models.DateField(verbose_name=_("Date"), db_index=True)
    expiration_date = models.DateField(verbose_name=_('Expiration Date'), db_index=True)

    costcenter = models.ForeignKey(FiCostCenter, blank=True, null=True, verbose_name=_("Cost Center"))
    current_account = models.ForeignKey(FiCurrentAccount, verbose_name=_('Current Account'))

    '''doc_content_type = models.ForeignKey(ContentType, null=True)
    doc_object_id = models.PositiveIntegerField(null=True)
    doc_content_object = GenericForeignKey('doc_content_type', 'doc_object_id')'''

    document_type = models.CharField(max_length=2, choices=ENTRY_DOC_TYPES, verbose_name=_("Document Type"), null=True)
    other_description = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Other"))
    document_number = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Document Number'))

    cheque = models.ForeignKey(FiCheque, blank=True, null=True)

    department = models.ForeignKey(MaDepartment, verbose_name=_('Department'))
    customer_supplier = models.ForeignKey(MaCustomerSupplier, null=True, blank=True, verbose_name=_('Customer/Supplier'))
    record = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Story'))
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Value'), default=0)
    interest = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Interest'), default=0)
    category = models.CharField(max_length=1, blank=True, null=True, choices=(('1', 'ONE'), ('2', 'TWO')))
    status = models.CharField(max_length=2, blank=True, choices=(('R', _('Receivable')), ('P', _('Payable')), ('RR', _('Received')),
                                                     ('PP', _('Paid'))))

    history = HistoricalRecords()

    def __unicode__(self):
        return str(self.id)

    def update_status(self):
        pass


    def get_costcenter_code(self):
        return self.costcenter.get_code()

    def get_customer_supplier_name(self):
        return self.customer_supplier.get_name()

    def get_formated_date(self):
        return self.date.strftime("%d/%m/%Y")

    def get_formated_expiration_date(self):
        return self.expiration_date.strftime("%d/%m/%Y")

    def get_formated_value(self):
        locale.setlocale(locale.LC_MONETARY, '')
        if self.costcenter.account.type == 'R':
            class_type = 'text-success'
        else:
            class_type = 'text-danger'
        return mark_safe('<span class="%s">%s</span>' % (class_type,  locale.currency(self.value)))

    def get_info_icons(self):
        write_off = ''
        if (self.fiwriteoff_set.exists()):
            balance = 0
            for wo in self.fiwriteoff_set.all():
                balance += wo.value
            if balance == (self.value+self.interest):
                write_off = '<span title="'+_('Wrote off')+'" class="fa fa-check-square text-info"></span>'
            elif balance > 0:
                write_off = '<span title="'+_('Wrote off')+'" class="fa fa-minus-square text-info"></span>'

        return '%s %s' % (self.costcenter.account.get_type_icon_only(), write_off)

    @permalink
    def get_absolute_url(self):
        return ('financial_entry_detail', (), {'pk': self.id})

    class Meta:
        verbose_name = _('Entry')
        get_latest_by = 'date'


'''
class FiDocInvoice(Model):
    description = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    date = models.DateField()
    entry = generic.GenericRelation(FiEntry, null=True)

class FiDocCheque(Model):
    person = models.ForeignKey(MaPerson, null=True, blank=True, verbose_name=_('Person'))
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Description'))
    bank = models.ForeignKey(MaBank, null=True, blank=True, verbose_name=_('Bank'))
    agency = models.CharField(max_length=20, null=True, blank=True, verbose_name=_('Agency'))
    current_account = models.CharField(max_length=20, null=True, blank=True, verbose_name=_('Current account'))
    expiration_date = models.DateField(null=True, blank=True, verbose_name=_('Expiration Date'))
    number = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Number'))
    entry = generic.GenericRelation(FiEntry, null=True)

class FiDocDuplicate(Model):
    number = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Number'))
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Description'))
    entry = generic.GenericRelation(FiEntry, null=True)

class FiDocReceipt(Model):
    number = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Number'))
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Description'))
    entry = generic.GenericRelation(FiEntry, null=True)

class FiDocPromissoryNote(Model):
    number = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Number'))
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Description'))
    entry = generic.GenericRelation(FiEntry, null=True)

class FiDocOther(Model):
    name = models.CharField(max_length=100)
    entry = generic.GenericRelation(FiEntry, null=True)
'''

class FiWriteOff(Model):
    date = models.DateField(null=True, blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    '''doc_content_type = models.ForeignKey(ContentType, null=True)
    doc_object_id = models.PositiveIntegerField(null=True)
    doc_content_object = GenericForeignKey('doc_content_type', 'doc_object_id')'''
    cheque = models.ForeignKey(FiCheque, null=True, blank=True)
    entry = models.ForeignKey(FiEntry, null=True)

    class Meta:
        verbose_name = _('Write off')
        gender = 'F'


class FiLastCurrentAccountBalance(Manager):
    def last_balances(self, current_account):
        set = super(FiLastCurrentAccountBalance, self).get_queryset().filter(current_account=current_account).order_by('-date')[:11]
        new_list = list(set)
        if len(set) == 1:
            new_list.insert(0, FiCurrentAccountBalance(date=set[0].date, record=_('Last Balance'), value=None, balance=0))
        else:
            last = set.last()
            new_list.remove(new_list[len(new_list)-1])
            new_list.insert(0, FiCurrentAccountBalance(date=last.date, record=_('Last Balance'), value=None, balance=last.balance))

        return new_list


class FiCurrentAccountBalance(Model):
    date = models.DateTimeField(verbose_name=_('Data'), db_index=True)
    record = models.CharField(max_length=255, verbose_name=_('Story'))
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Value'))
    balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Balance'))
    current_account = models.ForeignKey(FiCurrentAccount)
    write_off = models.ForeignKey(FiWriteOff)
    entry = models.ForeignKey(FiEntry)

    objects = FiLastCurrentAccountBalance()

    def get_formated_value(self):
        locale.setlocale(locale.LC_MONETARY, '')

        if self.value is None:
            return ''

        if self.value >= 0:
            result = '<span class="text-success">%s</span> <span class="text-success fa fa-plus"></span>'
        else:
            result = '<span class="text-danger">%s</span> <span class="text-success fa fa-minus"></span>'

        return mark_safe(result % locale.currency(self.value))

    def get_formated_balance(self):
        locale.setlocale(locale.LC_MONETARY, '')

        if self.balance >= 0:
            result = '<span class="text-success">%s</span> <span class="text-success fa fa-plus"></span>'
        else:
            result = '<span class="text-danger">%s</span> <span class="text-success fa fa-minus"></span>'

        return mark_safe(result % locale.currency(self.balance))


    @staticmethod
    def get_last_balance_for_account(account):
        return FiCurrentAccountBalance.objects.filter(current_account=account).order_by('-date').last()

    @staticmethod
    def get_last_date_balance_for_account(account, date):
        return FiCurrentAccountBalance.objects.filter(current_account=account, date=date).order_by('-date').last()

    @staticmethod
    def consolidate_balance(oldest_date):
        pass
