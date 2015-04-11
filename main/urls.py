from django.conf.urls import patterns, url, include
from main.views import MaDepartmentCreateView, MaDepartmentListView, MaDepartmentUpdateView, MaEmployeeListView, \
    MaEmployeeCreateView, MaEmployeeUpdateView, MaEmployeeFunctionListView, MaEmployeeFunctionCreateView, \
    MaEmployeeFunctionUpdateView, MaCustomerSupplierListView, MaCustomerSupplierCreateView, MaCustomerSupplierUpdateView, \
    MaEmployeeDetailView, MaCustomerSupplierDetailView, MaPersonListView, MaPersonCreateView, MaPersonUpdateView, \
    MaPersonDetailView, MaEquipmentListView, MaEquipmentCreateView, MaEquipmentDetailView, MaEquipmentUpdateView, \
    MaEquipmentTypeListView, MaEquipmentTypeCreateView, MaEquipmentTypeUpdateView, MaBankUpdateView, MaBankListView, \
    MaBankCreateView
from django.utils.translation import ugettext_lazy as _

urlpatterns = patterns('',
    url(_(r'^/employee_function$'), MaEmployeeFunctionListView.as_view(), name="main_employeefunction"),
    url(_(r'^/employee_function/add$'), MaEmployeeFunctionCreateView.as_view(), name="main_employeefunction_add"),
    url(_(r'^/employee_function/(?P<pk>[0-9]+)'),include([
        url(_(r'/edit$'), MaEmployeeFunctionUpdateView.as_view(), name="main_employeefunction_edit"),
    ])),
    url(_(r'^/department$'), MaDepartmentListView.as_view(), name="main_department"),
    url(_(r'^/department/add$'), MaDepartmentCreateView.as_view(), name="main_department_add"),
    url(_(r'^/department/(?P<pk>[0-9]+)'),include([
        url(_(r'/edit$'), MaDepartmentUpdateView.as_view(), name="main_department_edit"),
    ])),
    url(_(r'^/person$'), MaPersonListView.as_view(), name="main_person"),
    url(_(r'^/person/add$'), MaPersonCreateView.as_view(), name="main_person_add"),
    url(_(r'^/person/(?P<pk>[0-9]+)'),include([
        url(_(r'^[/]$'), MaPersonDetailView.as_view(), name="main_person_detail"),
        url(_(r'/edit$'), MaPersonUpdateView.as_view(), name="main_person_edit"),
    ])),
    url(_(r'^/employee$'), MaEmployeeListView.as_view(), name="main_employee"),
    url(_(r'^/employee/add$'), MaEmployeeCreateView.as_view(), name="main_employee_add"),
    url(_(r'^/employee/(?P<pk>[0-9]+)'),include([
        url(_(r'^[/]$'), MaEmployeeDetailView.as_view(), name="main_employee_detail"),
        url(_(r'^/edit$'), MaEmployeeUpdateView.as_view(), name="main_employee_edit"),
    ])),
    url(_(r'^/customer_supplier$'), MaCustomerSupplierListView.as_view(), name="main_customer_supplier"),
    url(_(r'^/customer_supplier/add$'), MaCustomerSupplierCreateView.as_view(), name="main_customer_supplier_add"),
    url(_(r'^/customer_supplier/(?P<pk>[0-9]+)'),include([
        url(_(r'^[/]$'), MaCustomerSupplierDetailView.as_view(), name="main_customer_supplier_detail"),
        url(_(r'/edit$'), MaCustomerSupplierUpdateView.as_view(), name="main_customer_supplier_edit"),
    ])),
    url(_(r'^/equipment$'), MaEquipmentListView.as_view(), name="main_equipment"),
    url(_(r'^/equipment/add$'), MaEquipmentCreateView.as_view(), name="main_equipment_add"),
    url(_(r'^/equipment/(?P<pk>[0-9]+)'),include([
        url(_(r'^[/]$'), MaEquipmentDetailView.as_view(), name="main_equipment_detail"),
        url(_(r'/edit$'), MaEquipmentUpdateView.as_view(), name="main_equipment_edit"),
    ])),
    url(_(r'^/equipment_type$'), MaEquipmentTypeListView.as_view(), name="main_equipmenttype"),
    url(_(r'^/equipment_type/add$'), MaEquipmentTypeCreateView.as_view(), name="main_equipmenttype_add"),
    url(_(r'^/equipment_type/(?P<pk>[0-9]+)'),include([
        url(_(r'/edit$'), MaEquipmentTypeUpdateView.as_view(), name="main_equipmenttype_edit"),
    ])),
    url(_(r'^/bank$'), MaBankListView.as_view(), name="main_bank"),
    url(_(r'^/bank/add$'), MaBankCreateView.as_view(), name="main_bank_add"),
    url(_(r'^/bank/(?P<pk>[0-9]+)'),include([
        url(_(r'/edit$'), MaBankUpdateView.as_view(), name="main_bank_edit"),
    ])),
)
