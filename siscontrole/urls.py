from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views
from django.conf import settings
from dashboard_view.views import DashboardOverviewView, DashboardProfileView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'siscontrole.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^select2/', include('django_select2.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', 'siscontrole.views.logout', name='logout'),
    url(r'^$', DashboardOverviewView.as_view(), name="dashboard_index"),
    url(r'^profile$', DashboardProfileView.as_view(), name="user_profile"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('crop_image.urls')),
    url(r'^main', include('main.urls'),),
    url(r'^financial', include('financial.urls'),),
)

if settings.DEBUG :
    urlpatterns += patterns('',
        (r'^uploaded_images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )