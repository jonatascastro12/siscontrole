# -*- coding: utf-8 -*-
import imghdr
import json
import os
from PIL import Image
from django.apps import apps
from django.conf.urls import url
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.temp import NamedTemporaryFile
from django.core.urlresolvers import reverse, reverse_lazy
from django.forms.widgets import Media
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic.base import ContextMixin, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, FormView, CreateView, DeleteView
from django.views.generic.list import ListView
from siscontrole import errors
from siscontrole.settings import INSTALLED_APPS, MEDIA_ROOT, MEDIA_URL


class DashboardMenu():
    app_list = [apps.get_app_config(app) for app in INSTALLED_APPS if not ("django" in app) and not ("nested" in app) and not ("bootstrap" in app) and not ("sorl" in app)]

    menu = [
        {'name': 'overview', 'icon_class': 'fa-dashboard', 'verbose_name': _('Overview'), 'link': '/'},
        {'name': 'main', 'icon_class': 'fa-users', 'verbose_name': _('Main'), 'children':
            [
                {'name': 'departments', 'verbose_name': _('Department'), 'link': reverse_lazy('main_department')},
                {'name': 'employee', 'verbose_name': _('Employee')},
                {'name': 'supplier', 'verbose_name': _('Supplier')},
                {'name': 'customer', 'verbose_name': _('Customer')},
            ]},

        {'name': 'financial', 'icon_class': 'fa-money', 'verbose_name': _('Financial'), 'children':
            [
                {'name': 'maintenance', 'verbose_name': 'Maintenance', 'children':
                    [
                        {'name': 'document_type', 'verbose_name': _('Document type'), 'link': '/financial/document_types'},
                        {'name': 'dolar', 'verbose_name': _('Dolar'), 'link': '/financial/dolar'},
                        {'name': 'bank', 'verbose_name': _('Bank'), 'link': '/financial/bank'},
                        {'name': 'current_account', 'verbose_name': _('Current account'), 'link': '/financial/current_account'},
                        {'name': 'account_groups', 'verbose_name': _('Account groups'), 'link': '/financial/account_group'},
                        {'name': 'account', 'verbose_name': _('Account'), 'link': '/financial/account'},
                        {'name': 'subaccount', 'verbose_name': _('Subaccount'), 'link': '/financial/subaccount'},
                        {'name': 'subaccount_type', 'verbose_name': _('Subaccount Type'), 'link': '/financial/subaccount_type'},
                        {'name': 'cost_center', 'verbose_name': _('Cost center'), 'link': '/financial/cost_center'},
                ]},
                {'name': 'entry', 'verbose_name': _('Entry'), 'link': '/financial/entry'},
            ]
        },
    ]

    def render(self, request=None, permission=None):
        output = u''
        for item in self.menu:
            link = item.get('link', '#')
            active = 'active' if link in request.path_info else ''
            icon_class = item.get('icon_class', '')
            verbose_name = item.get('verbose_name', item['name'])
            arrow = '<span class="fa arrow"></span>' if 'children' in item else ''
            output += u'<li><a href="{0}" class="{1}"><i class="fa {2} ' \
                      u'fa-fw"></i>{3} {4}</a>'.format(link, active, icon_class, verbose_name, arrow)
            if 'children' in item:
                output += u'<ul class="nav nav-second-level">'#.format(' open' if active != '' else '')
                for child_item in item['children']:
                    link = child_item.get('link', '#')
                    try:
                        active = 'active' if link in request.path_info else ''
                    except TypeError:
                        active = 'active' if link._proxy____args[0] in request.resolver_match.view_name else ''

                    icon_class = child_item.get('icon_class', '')
                    verbose_name = child_item.get('verbose_name', child_item['name'])
                    arrow = '<span class="fa arrow"></span>' if 'children' in child_item else ''
                    output += u'<li><a href="{0}" class="{1}"><i class="fa {2}' \
                              u'fa-fw"></i>{3} {4}</a>'.format(link, active, icon_class, verbose_name, arrow)
                    if 'children' in child_item:
                        output += u'<ul class="nav nav-third-level">'#.format(' open' if active != '' else '')
                        for third_level in child_item['children']:
                            link = third_level.get('link', '#')
                            active = 'active' if link in request.path_info else ''
                            icon_class = third_level.get('icon_class', '')
                            verbose_name = third_level.get('verbose_name', third_level['name'])
                            output += u'<li><a href="{0}" class="{1}"><i class="fa {2}' \
                                      u'fa-fw"></i>{3}</a></li>'.format(link, active, icon_class, verbose_name)
                        output += u'</ul>'
                    output += u'</li>'
                output += u'</ul>'
            output += u'</li>'
        return output

    def menu_list(self):
        mlist = []
        ''' mlist.append({'link': '/dashboard', 'app_verbose_name': _('Overview')})
        for app in self.app_list:
            models = get_models(get_app(app.label))
            app_obj = {'app': app, 'app_verbose_name': app.verbose_name,
                       'models': [{'verbose_name': m._meta.verbose_name_plural,
                        'link': m._meta.model_name } for m in models if m._meta.model_name in ['member', 'church']]}
            mlist.append(app_obj)
        '''
        return mlist

class DashboardView(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        menu = DashboardMenu()
        context['app_list'] = menu.menu_list()
        context['dashboard_menu'] = menu.render(self.request)
        context['media_css'] = Media()
        context['media_js'] = Media()

        context['page_name'] = self.model._meta.verbose_name_plural

        context['fields'] = self.model._meta.fields

        if self.fields:
            for f in context['fields']:
                if f.name not in self.fields:
                    context['fields'].remove(f)

        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DashboardView, self).dispatch(request, *args, **kwargs)

class DashboardListView(ListView, DashboardView):
    pass

class DashboardDetailView(DetailView, DashboardView):
    pass

class DashboardCreateView(CreateView, DashboardView):
    pass

class DashboardFormView(FormView, DashboardView):
    pass

class DashboardUpdateView(UpdateView, DashboardView):
    pass

class DashboardDeleteView(DeleteView, DashboardView):
    pass

@login_required
def dashboard(request):
    menu = DashboardMenu()
    return render(request, "dashboard_base.html", {"dashboard_menu": menu.render(request)})

def profile(request):
    menu = DashboardMenu()
    return render(request, "dashboard_base.html", {"dashboard_menu": menu.render(request)})

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

def image_upload(request):
    upload_to = ''
    if 'upload_to' in request.POST:
        upload_to = request.POST['upload_to']

    if request.POST and 'photo_crop_data' in request.POST and 'photo_original' in request.POST:

        im = Image.open(os.path.join(os.path.dirname(os.path.dirname(__file__)), request.POST['photo_original'].lstrip('/').replace('/','\\')))

        crop_data = json.loads(request.POST['photo_crop_data'])
        img_ratio = im.size[0]/float(crop_data["bounds"][0])

        crop_params = (int(round(crop_data['selectionPosition']['left']*img_ratio)),
                       int(round(crop_data['selectionPosition']['top']*img_ratio)),
                       int(round(crop_data['selectionPosition']['left']*img_ratio))+int(round(crop_data['selectionSize']*img_ratio)),
                       int(round(crop_data['selectionPosition']['top']*img_ratio))+int(round(crop_data['selectionSize']*img_ratio))
        )

        thumb_posfix = '_thumb_512'

        original_name, extension = os.path.splitext(im.filename)
        cropped_img = im.crop(crop_params)
        cropped_img.thumbnail((512, 512), Image.ANTIALIAS)
        cropped_img.save(original_name + thumb_posfix + extension)

        filename = os.path.splitext(os.path.split(im.filename)[1])[0]
        newfilename = filename + thumb_posfix + extension

        return HttpResponse(os.path.join(os.path.join(MEDIA_URL, upload_to), newfilename))


    if request.FILES and 'photo' in request.FILES:
        upload_full_path = os.path.join(MEDIA_ROOT, upload_to)

        if not os.path.exists(upload_full_path):
            os.makedirs(upload_full_path)
        upload = request.FILES['photo']
        original_name, extension = os.path.splitext(upload.name)
        f = NamedTemporaryFile(mode='w+b')
        upload.name = str(original_name) + '_' + os.path.split(f.name)[1] + str(extension)

        while os.path.exists(os.path.join(upload_full_path, upload.name)):
            f = NamedTemporaryFile(mode='w+b')
            upload.name = str(original_name) + '_' + os.path.split(f.name)[1] + str(extension)

        dest = open(os.path.join(upload_full_path, upload.name), 'wb')

        for chunk in upload.chunks():
            dest.write(chunk)
        dest.close()

        try:
            ext = imghdr.what(os.path.join(upload_full_path, upload.name))
            if ext not in ('jpeg', 'jpg', 'png'):
                return HttpResponse(status=406, content=errors.ImageNotJpgOrPngError().response_error())
            im = Image.open(os.path.join(upload_full_path, upload.name))
            if (im.size <= (512,512)):
                return HttpResponse(status=406, content=errors.ImageLessThan512().response_error())
        except IOError:
            return HttpResponse(status=406, content=errors.ImageNotRecognized().response_error())

        return HttpResponse(os.path.join(os.path.join(MEDIA_URL, upload_to), upload.name))
    return HttpResponse(status=405, content_type='application/json', content=errors.GetRequestNotPermitted.response_error())