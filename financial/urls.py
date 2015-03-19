from django.conf.urls import patterns, url, include
from django.utils.translation import ugettext_lazy as _

from financial.views import FiDocumentTypeListView, FiDocumentTypeCreateView, FiDocumentTypeUpdateView, \
    FiCurrentAccountUpdateView, FiCurrentAccountCreateView, FiCurrentAccountListView, FiAccountGroupListView, \
    FiAccountGroupCreateView, FiAccountGroupUpdateView, FiCurrentAccountDetailView, FiAccountGroupDetailView, \
    FiAccountListView, FiAccountCreateView, FiAccountDetailView, FiAccountUpdateView, FiSubaccountListView, \
    FiSubaccountCreateView, FiSubaccountDetailView, FiSubaccountUpdateView, FiSubaccountTypeListView, \
    FiSubaccountTypeCreateView, FiSubaccountTypeDetailView, FiSubaccountTypeUpdateView, FiCostCenterCreateView, \
    FiCostCenterDetailView, FiCostCenterUpdateView, FiCostCenterListView, FiEntryCreateView, FiEntryListView, \
    get_value_for_key, get_account_type

urlpatterns = patterns('',
    url(_(r'^/document_type$'), FiDocumentTypeListView.as_view(), name="financial_documenttype"),
    url(_(r'^/document_type/add$'), FiDocumentTypeCreateView.as_view(), name="financial_documenttype_add"),
    url(_(r'^/document_type/(?P<pk>[0-9]+)'), include([
        url(_(r'/edit$'), FiDocumentTypeUpdateView.as_view(), name="financial_documenttype_edit"),
    ])),
    url(_(r'^/current_account$'), FiCurrentAccountListView.as_view(), name="financial_currentaccount"),
    url(_(r'^/current_account/add$'), FiCurrentAccountCreateView.as_view(), name="financial_currentaccount_add"),
    url(_(r'^/current_account/(?P<pk>[0-9]+)'), include([
        url(_(r'[/]$'), FiCurrentAccountDetailView.as_view(), name="financial_currentaccount_detail"),
        url(_(r'/edit$'), FiCurrentAccountUpdateView.as_view(), name="financial_currentaccount_edit"),
    ])),
    url(_(r'^/account_group$'), FiAccountGroupListView.as_view(), name="financial_accountgroup"),
    url(_(r'^/account_group/add$'), FiAccountGroupCreateView.as_view(), name="financial_accountgroup_add"),
    url(_(r'^/account_group/(?P<pk>[0-9]+)'), include([
        url(_(r'[/]$'), FiAccountGroupDetailView.as_view(), name="financial_accountgroup_detail"),
        url(_(r'/edit$'), FiAccountGroupUpdateView.as_view(), name="financial_accountgroup_edit"),
    ])),
    url(_(r'^/account$'), FiAccountListView.as_view(), name="financial_account"),
    url(_(r'^/account/add$'), FiAccountCreateView.as_view(), name="financial_account_add"),
    url(_(r'^/account/(?P<pk>[0-9]+)'), include([
        url(_(r'[/]$'), FiAccountDetailView.as_view(), name="financial_account_detail"),
        url(_(r'/edit$'), FiAccountUpdateView.as_view(), name="financial_account_edit"),
    ])),
    url(_(r'^/subaccount$'), FiSubaccountListView.as_view(), name="financial_subaccount"),
    url(_(r'^/subaccount/add$'), FiSubaccountCreateView.as_view(), name="financial_subaccount_add"),
    url(_(r'^/subaccount/(?P<pk>[0-9]+)'), include([
        url(_(r'[/]$'), FiSubaccountDetailView.as_view(), name="financial_subaccount_detail"),
        url(_(r'/edit$'), FiSubaccountUpdateView.as_view(), name="financial_subaccount_edit"),
    ])),
    url(_(r'^/subaccount_type$'), FiSubaccountTypeListView.as_view(), name="financial_subaccounttype"),
    url(_(r'^/subaccount_type/add$'), FiSubaccountTypeCreateView.as_view(), name="financial_subaccounttype_add"),
    url(_(r'^/subaccount_type/(?P<pk>[0-9]+)'), include([
        url(_(r'[/]$'), FiSubaccountTypeDetailView.as_view(), name="financial_subaccounttype_detail"),
        url(_(r'/edit$'), FiSubaccountTypeUpdateView.as_view(), name="financial_subaccounttype_edit"),
    ])),
    url(_(r'^/cost_center$'), FiCostCenterListView.as_view(), name="financial_costcenter"),
    url(_(r'^/cost_center/add$'), FiCostCenterCreateView.as_view(), name="financial_costcenter_add"),
    url(_(r'^/cost_center/(?P<pk>[0-9]+)'), include([
        url(_(r'[/]$'), FiCostCenterDetailView.as_view(), name="financial_costcenter_detail"),
        url(_(r'/edit$'), FiCostCenterUpdateView.as_view(), name="financial_costcenter_edit"),
    ])),
    url(_(r'^/get_value_for_key'), get_value_for_key, name="financial_get_value_for_key"),
    url(_(r'^/get_account_type'), get_account_type, name="financial_get_account_type"),
    url(_(r'^/entry$'), FiEntryListView.as_view(), name="financial_entry"),
    url(_(r'^/entry/add$'), FiEntryCreateView.as_view(), name="financial_entry_add"),

)
