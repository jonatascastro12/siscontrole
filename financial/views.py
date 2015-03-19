from django.core.urlresolvers import reverse_lazy

# Create your views here.
from django.db.models.loading import get_model
from django.http.response import HttpResponse, HttpResponseServerError
from django.utils.translation import ugettext as _
from financial.forms import FiCurrentAccountForm, FiEntryForm, FiCostCenterForm
from financial.models import FiDocumentType, FiCurrentAccount, FiAccountGroup, FiAccount, FiSubaccount, FiSubaccountType, \
    FiCostCenter, FiEntry
from siscontrole.views import DashboardListView, DashboardCreateView, DashboardUpdateView, DashboardDetailView


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

    def get_context_data(self, **kwargs):
       context = super(FiEntryCreateView, self).get_context_data(**kwargs)
       context['costcenter_form'] = FiCostCenterForm()

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