from django.conf.urls import patterns, url, include
from main.views import MaDepartmentCreateView, MaDepartmentListView, MaDepartmentUpdateView, MaEmployeeListView, \
    MaEmployeeCreateView, MaEmployeeUpdateView, MaEmployeeFunctionListView, MaEmployeeFunctionCreateView, \
    MaEmployeeFunctionUpdateView, MaCustomerSupplierListView, MaCustomerSupplierCreateView, MaCustomerSupplierUpdateView, \
    MaEmployeeDetailView, MaCustomerSupplierDetailView, MaPersonListView, MaPersonCreateView, MaPersonUpdateView

urlpatterns = patterns('',
    url(r'^/employee_function$', MaEmployeeFunctionListView.as_view(), name="main_employee_function"),
    url(r'^/employee_function/add$', MaEmployeeFunctionCreateView.as_view(), name="main_employee_function_add"),
    url(r'^/employee_function/(?P<pk>[0-9]+)', include([
        url(r'/edit$', MaEmployeeFunctionUpdateView.as_view(), name="main_employee_function_edit"),
    ])),
    url(r'^/department$', MaDepartmentListView.as_view(), name="main_department"),
    url(r'^/department/add$', MaDepartmentCreateView.as_view(), name="main_department_add"),
    url(r'^/department/(?P<pk>[0-9]+)', include([
        url(r'/edit$', MaDepartmentUpdateView.as_view(), name="main_department_edit"),
    ])),
    url(r'^/person$', MaPersonListView.as_view(), name="main_person"),
    url(r'^/person/add$', MaPersonCreateView.as_view(), name="main_person_add"),
    url(r'^/person/(?P<pk>[0-9]+)', include([
        url(r'/edit$', MaPersonUpdateView.as_view(), name="main_person_edit"),
    ])),
    url(r'^/employee$', MaEmployeeListView.as_view(), name="main_employee"),
    url(r'^/employee/add$', MaEmployeeCreateView.as_view(), name="main_employee_add"),
    url(r'^/employee/(?P<pk>[0-9]+)', include([
        url(r'^[/]$', MaEmployeeDetailView.as_view(), name="main_employee_detail"),
        url(r'^/edit$', MaEmployeeUpdateView.as_view(), name="main_employee_edit"),
    ])),
    url(r'^/customer_supplier$', MaCustomerSupplierListView.as_view(), name="main_customer_supplier"),
    url(r'^/customer_supplier/add$', MaCustomerSupplierCreateView.as_view(), name="main_customer_supplier_add"),
    url(r'^/customer_supplier/(?P<pk>[0-9]+)', include([
        url(r'[/]$', MaCustomerSupplierDetailView.as_view(), name="main_customer_supplier_detail"),
        url(r'/edit$', MaCustomerSupplierUpdateView.as_view(), name="main_customer_supplier_edit"),
    ])),
)
