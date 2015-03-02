from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render

# Create your views here.
from main.models import MaDepartment
from siscontrole.views import DashboardFormView, DashboardCreateView, DashboardListView, DashboardDeleteView, \
    DashboardUpdateView


class MaDepartmentListView(DashboardListView):
    model = MaDepartment
    fields = ['id', 'name']

class MaDepartmentCreateView(DashboardCreateView):
    model = MaDepartment
    fields = ['name', 'description']

class MaDepartmentUpdateView(DashboardUpdateView):
    model = MaDepartment
    fields = ['name', 'description']

class MaDepartmentDeleteView(DashboardDeleteView):
    success_url = reverse_lazy('main_department')