from django.core.urlresolvers import reverse_lazy

# Create your views here.
from django.utils.translation import ugettext as _
from financial.forms import FiCurrentAccountForm
from financial.models import FiDocumentType, FiCurrentAccount, FiAccountGroup, FiAccount
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


''' Financial AccountGroup Views '''


class FiAccountListView(DashboardListView):
    model = FiAccount
    datatable_options = {
        'columns': [
            (_('Code'), 'get_code'),
            'name',
        ]
    }

class FiAccountCreateView(DashboardCreateView):
    model = FiAccount
    success_url = reverse_lazy('financial_accountgroup')

class FiAccountUpdateView(DashboardUpdateView):
    model = FiAccount
    success_url = reverse_lazy('financial_accountgroup')

class FiAccountDetailView(DashboardDetailView):
    model = FiAccount
    fields = ['name', 'type']