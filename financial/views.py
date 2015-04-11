# -*- coding: utf-8 -*-
from threading import Thread

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.db.models.loading import get_model
from django.http.response import HttpResponse, HttpResponseServerError, HttpResponseRedirect
from django.utils import timezone
from django.utils.translation import ugettext as _
from financial.filters import FiEntryFilter
from financial.forms import FiCurrentAccountForm, FiEntryForm, FiCostCenterForm, FiWriteOffFormset, \
    FiChequeForm
from financial.models import FiDocumentType, FiCurrentAccount, FiAccountGroup, FiAccount, FiSubaccount, FiSubaccountType, \
    FiCostCenter, FiEntry, FiCheque, FiCurrentAccountBalance
from dashboard_view.views import DashboardListView, DashboardCreateView, DashboardUpdateView, DashboardDetailView


''' Financial DocumentType Views '''


class FiDocumentTypeListView(DashboardListView):
    model = FiDocumentType
    datatable_options = {
        'columns': [
            'id',
            'name',
        ]
    }

class FiDocumentTypeCreateView(DashboardCreateView):
    model = FiDocumentType
    success_url = reverse_lazy('financial_documenttype')


class FiDocumentTypeUpdateView(DashboardUpdateView):
    model = FiDocumentType


class FiDocumentTypeDetailView(DashboardDetailView):
    model = FiDocumentType
    fields = ['name', 'type']
    

''' Financial CurrentAccount Views '''


class FiCurrentAccountListView(DashboardListView):
    model = FiCurrentAccount
    datatable_options = {
        'columns': [
            'id',
            'name',
            'bank',
            'agency',
            'number',
            (_('Balance'), 'get_formated_balance'),
        ]
    }

class FiCurrentAccountCreateView(DashboardCreateView):
    model = FiCurrentAccount
    success_url = reverse_lazy('financial_currentaccount')
    form_class = FiCurrentAccountForm

class FiCurrentAccountUpdateView(DashboardUpdateView):
    model = FiCurrentAccount
    success_url = reverse_lazy('financial_currentaccount')
    form_class = FiCurrentAccountForm

class FiCurrentAccountDetailView(DashboardDetailView):
    model = FiCurrentAccount
    fields = []

    def get_context_data(self, **kwargs):
        context = super(FiCurrentAccountDetailView, self).get_context_data(**kwargs)
        context['last_entries'] = context['object'].fientry_set.order_by('-date')[:10]
        context['last_balances'] = FiCurrentAccountBalance.objects.last_balances(context['object'], 10)


        return context


''' Financial AccountGroup Views '''


class FiAccountGroupListView(DashboardListView):
    model = FiAccountGroup
    datatable_options = {
        'columns': [
            (_('Code'), 'get_code'),
            'name',
        ]
    }

class FiAccountGroupCreateView(DashboardCreateView):
    model = FiAccountGroup
    success_url = reverse_lazy('financial_accountgroup')

class FiAccountGroupUpdateView(DashboardUpdateView):
    model = FiAccountGroup
    success_url = reverse_lazy('financial_accountgroup')

class FiAccountGroupDetailView(DashboardDetailView):
    model = FiAccountGroup
    fields = ['name', 'type']


''' Financial Account Views '''


class FiAccountListView(DashboardListView):
    model = FiAccount
    datatable_options = {
        'columns': [
            (_('Code'), 'get_code'),
            'name',
            (_('Type'), 'get_type_icon'),
        ]
    }

class FiAccountCreateView(DashboardCreateView):
    model = FiAccount
    success_url = reverse_lazy('financial_account')

class FiAccountUpdateView(DashboardUpdateView):
    model = FiAccount
    success_url = reverse_lazy('financial_account')

class FiAccountDetailView(DashboardDetailView):
    model = FiAccount
    fields = ['name', 'type']
    

''' Financial Subaccount Views '''


class FiSubaccountListView(DashboardListView):
    model = FiSubaccount
    datatable_options = {
        'columns': [
            (_('Code'), 'get_code'),
            'name',
        ]
    }

class FiSubaccountCreateView(DashboardCreateView):
    model = FiSubaccount
    success_url = reverse_lazy('financial_subaccount')

class FiSubaccountUpdateView(DashboardUpdateView):
    model = FiSubaccount
    success_url = reverse_lazy('financial_subaccount')

class FiSubaccountDetailView(DashboardDetailView):
    model = FiSubaccount
    fields = ['name', 'type']
    
    
''' Financial SubaccountType Views '''


class FiSubaccountTypeListView(DashboardListView):
    model = FiSubaccountType
    datatable_options = {
        'columns': [
            (_('Code'), 'get_code'),
            'name',
            'subaccount',
            (_('Nature'), 'get_nature_display')
        ]
    }

class FiSubaccountTypeCreateView(DashboardCreateView):
    model = FiSubaccountType
    success_url = reverse_lazy('financial_subaccounttype')

class FiSubaccountTypeUpdateView(DashboardUpdateView):
    model = FiSubaccountType
    success_url = reverse_lazy('financial_subaccounttype')

class FiSubaccountTypeDetailView(DashboardDetailView):
    model = FiSubaccountType
    fields = ['name', 'type']


''' Financial CostCenter Views '''


class FiCostCenterListView(DashboardListView):
    model = FiCostCenter
    datatable_options = {
        'columns': [
            (_('Code'), 'get_code'),
            'account_group',
            'account',
            'subaccount',
            'subaccount_type',
        ]
    }

class FiCostCenterCreateView(DashboardCreateView):
    model = FiCostCenter
    success_url = reverse_lazy('financial_costcenter')

class FiCostCenterUpdateView(DashboardUpdateView):
    model = FiCostCenter
    success_url = reverse_lazy('financial_costcenter')

class FiCostCenterDetailView(DashboardDetailView):
    model = FiCostCenter
    fields = ['name', 'type']

class FiEntryDetailView(DashboardDetailView):
    model = FiEntry
    fields = ['name', 'type']

class FiEntryListView(DashboardListView):
    model = FiEntry
    datatable_options = {
        'columns': [
            'date',
            'expiration_date',
            (_('Date'), 'get_formated_date'),
            #(_('Cost Center'), 'get_costcenter_code'),
            (_('Customer/Supplier'), 'get_customer_supplier_name'),
            'record',
            'current_account',
            'document_type',
            (_('Doc'), 'get_document_type_display'),
            (_('Value'), 'get_formated_value'),
            (_('Exp. Date'), 'get_formated_expiration_date'),
            (' ', 'get_info_icons'),
        ],
        'hidden_columns': ['date', 'expiration_date', 'document_type']
    }

    #   (LABEL,                         FIELD_NAME,          FILTER_TYPE,        CHOICES)
    filters = [
        (_('Date Range'),               'date',             'date_range'),
        (_('Expiration Date Range'),    'expiration_date',  'date_range'),
        (_('Document Type'),            'document_type',    'checkbox_choice'),
        (_('Status'),                   'status',           'checkbox_choice'),
        'record',
    ]
    filter_class = FiEntryFilter

    actions = [
        'remove_object',
        'print_individual',
        'auto_writeoff'
    ]

class FiEntryCreateView(DashboardCreateView):
    model = FiEntry
    form_class = FiEntryForm
    success_url = reverse_lazy('financial_entry')

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        costcenter_form = FiCostCenterForm(request.POST)
        writeoff_formset = FiWriteOffFormset(request.POST)
        entry_cheque_form = FiChequeForm(request.POST)

        if form.is_valid() and costcenter_form.is_valid():
            cc = costcenter_form.instance
            cc = FiCostCenter.objects.filter(account_group=cc.account_group, account=cc.account, subaccount=cc.subaccount, subaccount_type=cc.subaccount_type).first()
            form.instance.costcenter = cc

            cheque_valid = True
            if form.cleaned_data.get('document_type', None) == 'C' and form.cleaned_data.get('cheque', None) is None and not entry_cheque_form.is_valid():
                cheque_valid = False

            if not cheque_valid:
                return self.form_invalid(form, costcenter_form, writeoff_formset, entry_cheque_form)
            return self.form_valid(form, costcenter_form, writeoff_formset, entry_cheque_form)
        else:
            return self.form_invalid(form, costcenter_form, writeoff_formset, entry_cheque_form)

    @transaction.atomic()
    def form_valid(self, form, costcenter_form, writeoff_formset, entry_cheque_form):
        if form.cleaned_data.get('document_type') == 'C':
            if form.cleaned_data.get('cheque', None) is None:
                cheque = entry_cheque_form.save()
                form.instance.cheque = cheque

        self.object = form.save()

        balance = 0
        balances_to_save = []
        oldest_date = timezone.now().date()

        for wo in writeoff_formset:
            if wo.is_valid():
                balance += wo.instance.value
                wo.instance.entry = self.object
                wo_object = wo.save()
                value = 0
                if form.instance.costcenter.account.type == 'E':
                    value = -wo.instance.value
                else:
                    value = wo.instance.value

                new_balance = FiCurrentAccountBalance(
                    date=wo.instance.date,
                    value=value,
                    record=(form.instance.get_document_type_display() if not wo.instance.cheque else 'CHEQUE') + ': ' + form.instance.record,
                    balance=balance,
                    write_off=wo_object,
                    current_account=form.instance.current_account
                )
                balances_to_save.append(new_balance)
            else:
                return self.form_invalid(form, costcenter_form, writeoff_formset, entry_cheque_form)

        total = self.object.value + self.object.interest
        if total == balance and self.object.costcenter.account.type == 'E':
            self.object.status = 'PP'
        elif total == balance and self.object.costcenter.account.type == 'R':
            self.object.status = 'RR'
        elif total != balance and self.object.costcenter.account.type == 'E':
            self.object.status = 'P'
        else:
            self.object.status = 'R'

        self.object.save()

        for b in balances_to_save:
            last_balance = FiCurrentAccountBalance.get_last_date_balance_for_account(b.current_account, b.date)
            b.entry = self.object
            b.balance = (0 if last_balance is None else last_balance.balance) + b.value
            b.save()
            self.object.current_account.balance = self.object.current_account.balance + b.value
            self.object.current_account.save()

        FiCurrentAccountBalance.consolidate_balance(self.object.current_account)

        messages.success(self.request, _('Entry created successfully'))
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, costcenter_form, writeoff_formset, entry_cheque_form):
        return self.render_to_response(self.get_context_data(form=form, costcenter_form=costcenter_form, writeoff_formset=writeoff_formset, entry_cheque_form=entry_cheque_form))

    def get_context_data(self, **kwargs):
        context = super(FiEntryCreateView, self).get_context_data(**kwargs)
        context['costcenter_form'] = kwargs.get('costcenter_form', FiCostCenterForm())
        context['writeoff_formset'] = kwargs.get('writeoff_formset', FiWriteOffFormset())
        context['entry_cheque_form'] = kwargs.get('entry_cheque_form', FiChequeForm())
        return context


class FiEntryUpdateView(DashboardUpdateView):
    model = FiEntry
    form_class = FiEntryForm
    success_url = reverse_lazy('financial_entry')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        costcenter_form = FiCostCenterForm(request.POST, instance=self.object.costcenter)
        writeoff_formset = FiWriteOffFormset(request.POST, instance=self.object)
        entry_cheque_form = FiChequeForm(request.POST, instance=self.object.cheque)

        if form.is_valid() and costcenter_form.is_valid():
            cc = costcenter_form.instance
            cc = FiCostCenter.objects.filter(account_group=cc.account_group, account=cc.account, subaccount=cc.subaccount, subaccount_type=cc.subaccount_type).first()
            form.instance.costcenter = cc

            cheque_valid = True
            if form.cleaned_data.get('document_type', None) == 'C' and form.cleaned_data.get('cheque', None) is None and not entry_cheque_form.is_valid():
                cheque_valid = False

            if not cheque_valid:
                return self.form_invalid(form, costcenter_form, writeoff_formset, entry_cheque_form)
            return self.form_valid(form, costcenter_form, writeoff_formset, entry_cheque_form)
        else:
            return self.form_invalid(form, costcenter_form, writeoff_formset, entry_cheque_form)

    @transaction.atomic()
    def form_valid(self, form, costcenter_form, writeoff_formset, entry_cheque_form):
        if form.cleaned_data.get('document_type') == 'C':
            if form.cleaned_data.get('cheque', None) is None:
                cheque = entry_cheque_form.save()
                form.instance.cheque = cheque

        balance = 0
        balances_to_save = []
        oldest_date = timezone.now().date()

        for wo in writeoff_formset:
            if wo.is_valid():
                balance += wo.instance.value
                wo_object = wo.save()
                value = 0
                if form.instance.costcenter.account.type == 'E':
                    value = -wo.instance.value
                else:
                    value = wo.instance.value

                new_balance = FiCurrentAccountBalance(
                    date=wo.instance.date,
                    value=value,
                    record=(form.instance.get_document_type_display() if not wo.instance.cheque else 'CHEQUE') + ': ' + form.instance.record,
                    balance=balance,
                    write_off=wo_object,
                    current_account=form.instance.current_account
                )
                balances_to_save.append(new_balance)
                if oldest_date > wo.instance.date:
                    oldest_date = wo.instance.date

        total = form.instance.value + form.instance.interest
        if total == balance and form.instance.costcenter.account.type == 'E':
            form.instance.status = 'PP'
        elif total == balance and form.instance.costcenter.account.type == 'R':
            form.instance.status = 'RR'
        elif total != balance and form.instance.costcenter.account.type == 'E':
            form.instance.status = 'P'
        else:
            form.instance.status = 'R'

        self.object = form.save()

        for b in balances_to_save:
            obj = FiCurrentAccountBalance.objects.filter(write_off=b.write_off)
            if obj.exists():
                balance_obj = obj.first()
                b.id = balance_obj.id
                self.object.current_account.balance = self.object.current_account.balance - balance_obj.value
                last_balance = b.get_previous()
            else:
                last_balance = FiCurrentAccountBalance.get_last_date_balance_for_account(b.current_account, b.date)
            b.entry = self.object
            b.balance = (0 if last_balance is None else last_balance.balance) + b.value
            b.save()
            self.object.current_account.balance = self.object.current_account.balance + b.value
            self.object.current_account.save()

        thread = Thread(target=FiCurrentAccountBalance.consolidate_balance, args=(self.object.current_account, ))
        thread.start()

        messages.success(self.request, _('Entry updated successfully'))
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, costcenter_form, writeoff_formset, entry_cheque_form):
        return self.render_to_response(self.get_context_data(form=form, costcenter_form=costcenter_form, writeoff_formset=writeoff_formset, entry_cheque_form=entry_cheque_form))

    def get_context_data(self, **kwargs):
        context = super(FiEntryUpdateView, self).get_context_data(**kwargs)
        context['costcenter_form'] = kwargs.get('costcenter_form', FiCostCenterForm(instance=self.object.costcenter))


        context['writeoff_formset'] = kwargs.get('writeoff_formset', FiWriteOffFormset(instance=self.object))
        context['entry_cheque_form'] = kwargs.get('entry_cheque_form', FiChequeForm(instance=self.object.cheque))
        return context


''' Financial Cheque Views '''


class FiChequeListView(DashboardListView):
    model = FiCheque
    datatable_options = {
        'columns': [
            (_('#'), 'id'),
            'cheque_bank',
            'cheque_agency',
            (_('Name'), 'get_cheque_name'),
            'cheque_number',
            ('Expiration Date', 'cheque_expiration_date'),
            ('Value', 'get_formated_value'),
        ]
    }
    filters = {
        'cheque_number',
        (_('Expiration Date Range'),    'cheque_expiration_date',  'date_range'),
    }

    def get_column_Expiration_Date_data(self, instance, *args, **kwargs):
        return instance.cheque_expiration_date.strftime("%d/%m/%Y")

class FiChequeCreateView(DashboardCreateView):
    model = FiCheque
    success_url = reverse_lazy('financial_cheque')

class FiChequeUpdateView(DashboardUpdateView):
    model = FiCheque
    success_url = reverse_lazy('financial_cheque')

class FiChequeDetailView(DashboardDetailView):
    model = FiCheque
    fields = ['name', 'type']



def get_value_for_key(request):
    if request.GET:
        id = request.GET.get('id', None)
        key = request.GET.get('key', None)

        if id is None or key is None:
            value = '<span class="text-danger">%s</span>' % _("Something went wrong.")
            return HttpResponse(value)

        model_name = id.replace('id_', '').replace('_', '')

        Model = get_model('financial', 'fi'+model_name)

        obj = Model.objects.filter(id=key).first()

        if obj is not None:
            value='<span class="text-success">%s</span>' % obj.name
        else:
            value='<span class="text-danger">%s</span>' % (Model._meta.verbose_name + ' ' + _("not found"))
            return HttpResponse(value, status=404)
    return HttpResponse(value)

def get_account_type(request):
    if request.GET:
        account_id = request.GET.get('account_id', None)

        if account_id is None:
            return HttpResponse('', status=403)

        Model = FiAccount

        obj = Model.objects.filter(id=account_id).first()
        if obj is not None:
            type = obj.type
            if type == 'E':
                value = '<span class="text-danger"><span class="fa fa-level-down"></span>%s</span>' % (_('Expense'))
            else:
                value = '<span class="text-success"><span class="fa fa-level-up"></span>%s</span>' % (_('Revenue'))
            return HttpResponse(value)
        else:
            return HttpResponse(status=404)
    return HttpResponse('', status=403)