# -*- coding: utf-8 -*-

from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.db.models.loading import get_model
from django.http.response import HttpResponse, HttpResponseServerError, HttpResponseRedirect
from django.utils.translation import ugettext as _
from financial.forms import FiCurrentAccountForm, FiEntryForm, FiCostCenterForm, FiWriteOffFormset, \
    FiChequeForm
from financial.models import FiDocumentType, FiCurrentAccount, FiAccountGroup, FiAccount, FiSubaccount, FiSubaccountType, \
    FiCostCenter, FiEntry
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
            'balance',
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
    fields = ['name', 'type']


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
            'name',
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
    

class FiEntryListView(DashboardListView):
    model = FiEntry
    datatable_options = {
        'columns': [
            (_('Code'), 'get_code'),
            'client_supplier',
            (_('Cost Center'), 'get_costcenter_code'),
            'document_type',
            'value',
        ]
    }

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
            if form.cleaned_data.get('document_type') == 'C' and not entry_cheque_form.is_valid():
                cheque_valid = False
            if not cheque_valid:
                return self.form_invalid(form, costcenter_form, writeoff_formset, entry_cheque_form)
            return self.form_valid(form, costcenter_form, writeoff_formset, entry_cheque_form)
        else:
            return self.form_invalid(form, costcenter_form, writeoff_formset, entry_cheque_form)

    def form_valid(self, form, costcenter_form, writeoff_formset, entry_cheque_form):
        if form.cleaned_data.get('document_type') == 'C':
            cheque = entry_cheque_form.save()
            form.instance.cheque = cheque

        balance = 0
        for wo in writeoff_formset:
            if wo.is_valid():
                balance += wo.instance.value
                wo.save()

        if form.instance.value == balance and form.instance.costcenter.account == 'E':
            form.instance.status = 'PP'
        elif form.instance.value == balance and form.instance.costcenter.account == 'R':
            form.instance.status = 'RR'
        elif form.instance.value != balance and form.instance.costcenter.account == 'E':
            form.instance.status = 'P'
        else:
            form.instance.status = 'R'

        self.object = form.save()

        #TODO Debitar/creditar CONTA

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