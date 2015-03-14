from django.conf.urls import patterns, url, include
from financial.views import FiDocumentTypeListView, FiDocumentTypeCreateView, FiDocumentTypeUpdateView, \
    FiCurrentAccountUpdateView, FiCurrentAccountCreateView, FiCurrentAccountListView, FiAccountGroupListView, \
    FiAccountGroupCreateView, FiAccountGroupUpdateView, FiCurrentAccountDetailView, FiAccountGroupDetailView, \
    FiAccountListView, FiAccountCreateView, FiAccountDetailView, FiAccountUpdateView

urlpatterns = patterns('',
    url(r'^/document_type$', FiDocumentTypeListView.as_view(), name="financial_documenttype"),
    url(r'^/document_type/add$', FiDocumentTypeCreateView.as_view(), name="financial_documenttype_add"),
    url(r'^/document_type/(?P<pk>[0-9]+)', include([
        url(r'/edit$', FiDocumentTypeUpdateView.as_view(), name="financial_documenttype_edit"),
    ])),
    url(r'^/current_account$', FiCurrentAccountListView.as_view(), name="financial_currentaccount"),
    url(r'^/current_account/add$', FiCurrentAccountCreateView.as_view(), name="financial_currentaccount_add"),
    url(r'^/current_account/(?P<pk>[0-9]+)', include([
        url(r'[/]$', FiCurrentAccountDetailView.as_view(), name="financial_currentaccount_detail"),
        url(r'/edit$', FiCurrentAccountUpdateView.as_view(), name="financial_currentaccount_edit"),
    ])),
    url(r'^/account_group$', FiAccountGroupListView.as_view(), name="financial_accountgroup"),
    url(r'^/account_group/add$', FiAccountGroupCreateView.as_view(), name="financial_accountgroup_add"),
    url(r'^/account_group/(?P<pk>[0-9]+)', include([
        url(r'[/]$', FiAccountGroupDetailView.as_view(), name="financial_accountgroup_detail"),
        url(r'/edit$', FiAccountGroupUpdateView.as_view(), name="financial_accountgroup_edit"),
    ])),
    url(r'^/account$', FiAccountListView.as_view(), name="financial_account"),
    url(r'^/account/add$', FiAccountCreateView.as_view(), name="financial_account_add"),
    url(r'^/account/(?P<pk>[0-9]+)', include([
        url(r'[/]$', FiAccountDetailView.as_view(), name="financial_account_detail"),
        url(r'/edit$', FiAccountUpdateView.as_view(), name="financial_account_edit"),
    ])),
)
