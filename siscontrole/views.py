# -*- coding: utf-8 -*-
import imghdr
import json
import os
from PIL import Image
from datatableview.views import DatatableMixin
from django.apps import apps
from django.conf.urls import url
from django.contrib import auth, messages
from django.contrib.admin.models import LogEntry
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.temp import NamedTemporaryFile
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models.fields import Field, FieldDoesNotExist
from django.forms.widgets import Media
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.template.base import TemplateDoesNotExist
from django.template.defaultfilters import dictsort
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _, pgettext
from django.views.generic.base import ContextMixin, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, FormView, CreateView, DeleteView
from django.views.generic.list import ListView
import six
from siscontrole import errors
from siscontrole.settings import INSTALLED_APPS, MEDIA_ROOT, MEDIA_URL


class DashboardMenu():
    app_list = [apps.get_app_config(app) for app in INSTALLED_APPS if
                not ("django" in app) and not ("nested" in app) and not ("bootstrap" in app) and not ("sorl" in app)]

    menu = [
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
                        {'name': 'subaccount', 'verbose_name': _('Subaccount'), 'link': reverse_lazy('financial_subaccount')},
                        {'name': 'subaccount_type', 'verbose_name': _('Subaccount Type'),
                         'link': reverse_lazy('financial_subaccounttype')},
                        {'name': 'cost_center', 'verbose_name': _('Cost center'), 'link': reverse_lazy('financial_costcenter')},
                    ]},
                {'name': 'entry', 'verbose_name': _('Entry'), 'link': reverse_lazy('financial_entry')},
            ]
        },
    ]

    def render(self, request=None, permission=None):
        output = u''
        for item in self.menu:
            link = item.get('link', '#')
            try:
                active = 'active' if link == request.path_info else ''
            except TypeError:
                active = 'active' if link._proxy____args[0] == request.resolver_match.view_name else ''
            icon_class = item.get('icon_class', '')
            verbose_name = item.get('verbose_name', item['name'])
            arrow = '<span class="fa arrow"></span>' if 'children' in item else ''
            output += u'<li><a href="{0}" class="{1}"><i class="fa {2} ' \
                      u'fa-fw"></i>{3} {4}</a>'.format(link, '', icon_class, verbose_name, arrow)
            if 'children' in item:
                item['children'].sort()
                output += u'<ul class="nav nav-second-level">'  # .format(' open' if active != '' else '')
                for child_item in item['children']:
                    link = child_item.get('link', '#')
                    try:
                        active = 'active' if link == request.path_info else ''
                    except TypeError:
                        active = 'active' if link._proxy____args[0] == request.resolver_match.view_name else ''

                    icon_class = child_item.get('icon_class', '')
                    verbose_name = child_item.get('verbose_name', child_item['name'])
                    arrow = '<span class="fa arrow"></span>' if 'children' in child_item else ''
                    output += u'<li><a href="{0}" class="{1}"><i class="fa {2}' \
                              u'fa-fw"></i>{3} {4}</a>'.format(link, '', icon_class, verbose_name, arrow)
                    if 'children' in child_item:
                        output += u'<ul class="nav nav-third-level">'  # .format(' open' if active != '' else '')
                        for third_level in child_item['children']:
                            link = third_level.get('link', '#')
                            try:
                                active = 'active' if link == request.path_info else ''
                            except TypeError:
                                active = 'active' if link._proxy____args[0] == request.resolver_match.view_name else ''
                            icon_class = third_level.get('icon_class', '')
                            verbose_name = third_level.get('verbose_name', third_level['name'])
                            output += u'<li><a href="{0}" class="{1}"><i class="fa {2}' \
                                      u'fa-fw"></i>{3}</a></li>'.format(link, '', icon_class, verbose_name)
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

        try:
            get_template(self.model._meta.app_label + '/' + self.model._meta.model_name + self.template_name_suffix + '.html')
        except TemplateDoesNotExist:
            self.template_name = 'generics/dashboard' + self.template_name_suffix + '.html'

        context['app_list'] = menu.menu_list()
        context['dashboard_menu'] = menu.render(self.request)
        context['media_css'] = Media()
        context['media_js'] = Media()

        context['list_view'] = self.request.resolver_match.view_name. \
            replace('_edit', '').replace('_add', '').replace('_detail', '')
        context['add_view'] = self.request.resolver_match.view_name. \
                                  replace('_edit', '').replace('_add', '').replace('_detail', '') + '_add'
        context['detail_view'] = self.request.resolver_match.view_name. \
                                     replace('_edit', '').replace('_add', '').replace('_detail', '') + '_detail'
        context['edit_view'] = self.request.resolver_match.view_name. \
                                   replace('_edit', '').replace('_add', '').replace('_detail', '') + '_edit'


        new_title = (pgettext('female', 'New') if hasattr(self.model._meta, 'gender') and self.model._meta.gender == 'F' else\
            pgettext('male', 'New')) + u' ' + self.model._meta.verbose_name


        if self.template_name_suffix == '_form' and self.object:
            context[
                'page_name'] = self.model._meta.verbose_name + u' <small>' + self.object.__unicode__() + \
                               u' <span class="label label-warning">' + _('Editing') + u'</span></small> '
        elif self.template_name_suffix == '_detail':
            context['page_name'] = self.model._meta.verbose_name + u' <small>' + self.object.__unicode__() + \
                                   u'</small><a href="' + reverse(context['edit_view'], None, (),
                                                                  {'pk': self.object.pk}) + \
                                   u'" class="btn pull-right btn-primary">' + \
                                   _('Editar') + u'</a>'
        elif self.template_name_suffix == '_form':
            context['page_name'] = new_title
        else:
            context['page_name'] = self.model._meta.verbose_name_plural + \
                                   u'<a href="' + reverse(context['add_view']) + \
                                   u'" class="btn pull-right btn-success">' + \
                                   new_title + u'</a>'

        fields = list(self.model._meta.fields)
        context['fields'] = []

        if hasattr(self, 'datatable_options'):
            if self.datatable_options is not None:
                self.fields = self.datatable_options['columns']


        if self.fields:
            '''for f in fields:
                if f.name in self.fields:
                    context['fields'].append(f)'''

            for f in self.fields:
                if type(f) is not tuple and isinstance(f, six.string_types):
                    try:
                        context['fields'].append(self.model._meta.get_field_by_name(f)[0])
                    except FieldDoesNotExist:
                        if hasattr(self.model, f):
                            context['fields'].append(Field(verbose_name=f.title(), name=f))
                else:
                    try:
                        field = self.model._meta.get_field_by_name(f[1])[0]
                        field.verbose_name = f[0]
                        context['fields'].append(field)
                    except FieldDoesNotExist:
                        if hasattr(self.model, f[1]):
                            context['fields'].append(Field(verbose_name=f[0].title(), name=f[1]))

        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DashboardView, self).dispatch(request, *args, **kwargs)


class DashboardListView(DatatableMixin, ListView, DashboardView):
    def get_datatable_options(self):
        if type(self.datatable_options) is not dict:
            self.datatable_options = {}
        self.datatable_options["structure_template"] = "datatableview/bootstrap_structure.html"
        return self.datatable_options

    def get_column_data(self, i, name, instance):
        """ Finds the backing method for column ``name`` and returns the generated data. """
        values = super(DashboardListView, self).get_column_data(i, name, instance)

        if hasattr(instance._meta.model, 'get_absolute_url'):
            values = (u'<a href="%s">%s</a>' % (instance.get_absolute_url(), values[0]), values[1])

        return values

    def delete(self, request):
        if (isinstance(request.body, six.string_types)):
            data = json.loads(request.body)
            ids = data.get('ids', None)
            try:
                selected_objects = self.model.objects.filter(id__in=ids).all()
                selected_objects.delete()
                messages.success(self.request, _('Deleted successfully!'))
                return HttpResponse(status=200)
            except:
                raise
                return HttpResponse(status=401)


class DashboardDetailView(DetailView, DashboardView):
    pass


class DashboardCreateView(CreateView, DashboardView):
    def form_valid(self, form):

        model_name = self.model._meta.verbose_name

        if self.object:
            object_name = ' ' + self.object.__unicode__() + ' '
        else:
            object_name = ' ' + form.instance.__unicode__() + ' '

        # LogEntry.objects.log_action(self.request.user.id, )
        messages.success(self.request, message=model_name + object_name + _('created successfully!'))
        return super(DashboardCreateView, self).form_valid(form)


class DashboardFormView(FormView, DashboardView):
    pass


class DashboardUpdateView(UpdateView, DashboardView):
    def form_valid(self, form):
        model_name = self.model._meta.verbose_name
        object_name = self.object.__unicode__()

        messages.success(self.request, message=model_name + ' ' + object_name + _(' updated successfully!'))
        return super(DashboardUpdateView, self).form_valid(form)


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
        im = Image.open(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                     request.POST['photo_original'].lstrip('/').replace('/', '\\')))

        crop_data = json.loads(request.POST['photo_crop_data'])
        img_ratio = im.size[0] / float(crop_data["bounds"][0])

        crop_params = (int(round(crop_data['selectionPosition']['left'] * img_ratio)),
                       int(round(crop_data['selectionPosition']['top'] * img_ratio)),
                       int(round(crop_data['selectionPosition']['left'] * img_ratio)) + int(
                           round(crop_data['selectionSize'] * img_ratio)),
                       int(round(crop_data['selectionPosition']['top'] * img_ratio)) + int(
                           round(crop_data['selectionSize'] * img_ratio))
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
            if (im.size <= (512, 512)):
                return HttpResponse(status=406, content=errors.ImageLessThan512().response_error())
        except IOError:
            return HttpResponse(status=406, content=errors.ImageNotRecognized().response_error())

        return HttpResponse(os.path.join(os.path.join(MEDIA_URL, upload_to), upload.name))
    return HttpResponse(status=405, content_type='application/json',
                        content=errors.GetRequestNotPermitted.response_error())