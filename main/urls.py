from django.conf.urls import patterns, url, include
from main.views import MaDepartmentCreateView, MaDepartmentListView, MaDepartmentUpdateView

urlpatterns = patterns('',
    url(r'^/department', MaDepartmentListView.as_view(), name="main_department"),
    url(r'^/department/add$', MaDepartmentCreateView.as_view(), name="main_department_add"),
    url(r'^/department/(?P<pk>[0-9]+)', include([
        url(r'/edit$', MaDepartmentUpdateView.as_view(), name="main_department_edit"),
    ]))
)
