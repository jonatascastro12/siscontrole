# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from dashboard_view.views import DashboardMenu, DashboardView

menu_dict = [
    {'name': 'overview', 'icon_class': 'fa-dashboard', 'verbose_name': _('Overview'),
     'link': reverse_lazy('dashboard_index')},
    {'name': 'main', 'icon_class': 'fa-users', 'verbose_name': _('Main'), 'children':
        [
            {'name': 'person', 'verbose_name': _('Person'), 'link': reverse_lazy('main_person')},
            {'name': 'employee', 'verbose_name': _('Employee'), 'link': reverse_lazy('main_employee')},
            {'name': 'customer_supplier', 'verbose_name': _('Customer/Supplier'),
             'link': reverse_lazy('main_customer_supplier')},
            {'name': 'equipment', 'verbose_name': _('Equipment'), 'link': reverse_lazy('main_equipment')},
            {'name': 'maintenance', 'verbose_name': _('Maintenance'), 'children':
                [
                    {'name': 'departments', 'verbose_name': _('Department'),
                     'link': reverse_lazy('main_department')},
                    {'name': 'employee_function', 'verbose_name': _('Employee Function'),
                     'link': reverse_lazy('main_employeefunction')},
                    {'name': 'equipment_type', 'verbose_name': _('Employee Type'),
                     'link': reverse_lazy('main_equipmenttype')},
                    {'name': 'bank', 'verbose_name': _('Bank'),
                     'link': reverse_lazy('main_bank')},
                ]},
        ]},

    {'name': 'financial', 'icon_class': 'fa-money', 'verbose_name': _('Financial'), 'children':
        [
            {'name': 'maintenance', 'verbose_name': _('Maintenance'), 'children':
                [
                    {'name': 'document_type', 'verbose_name': _('Document type'),
                     'link': reverse_lazy('financial_documenttype')},
                    {'name': 'current_account', 'verbose_name': _('Current account'),
                     'link': reverse_lazy('financial_currentaccount')},
                    {'name': 'account_groups', 'verbose_name': _('Account groups'),
                     'link': reverse_lazy('financial_accountgroup')},
                    {'name': 'account', 'verbose_name': _('Account'), 'link': reverse_lazy('financial_account')},
                    {'name': 'subaccount', 'verbose_name': _('Subaccount'),
                     'link': reverse_lazy('financial_subaccount')},
                    {'name': 'subaccount_type', 'verbose_name': _('Subaccount Type'),
                     'link': reverse_lazy('financial_subaccounttype')},
                    {'name': 'cost_center', 'verbose_name': _('Cost center'),
                     'link': reverse_lazy('financial_costcenter')},
                ]},
            {'name': 'entry', 'verbose_name': _('Entry'), 'link': reverse_lazy('financial_entry')},
        ]
     },
]

DashboardView.menu = DashboardMenu(menu=menu_dict)

def logout(request):
    auth.logout(request)
    return redirect('/login')

def login(request):
    if (request.method == 'GET'):
        return render(request, "login.html")
    else:
        next = request.GET.get('next', '')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if '@' in username:
            user = User.objects.filter(email=username).first()
            if user is not None:
                username = user.username
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                if next:
                    return redirect(next)
                return redirect('/dashboard/overview')
            else:
                return render(request, 'login.html', {'error': "Usuário não está ativo."})
        else:
            return render(request, 'login.html', {'error': "Usuário ou senha inválidos."})