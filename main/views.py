from datatableview.views import DatatableMixin
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.utils.translation import ugettext as _
from main.forms import MaEmployeeForm, MaPersonForm, MaCustomerSupplierForm, MaMultiPersonForm, MaBankAccountFormset
from main.models import MaDepartment, MaEmployee, MaEmployeeFunction, MaCustomerSupplier, MaPerson, MaEquipment, \
    MaEquipmentType, MaBank
from dashboard_view.views import DashboardCreateView, DashboardListView, \
    DashboardUpdateView, DashboardDetailView


''' Main Equipment Views '''


class MaEquipmentListView(DashboardListView):
    model = MaEquipment
    fields = ['id', 'name']


class MaEquipmentCreateView(DashboardCreateView):
    model = MaEquipment


class MaEquipmentUpdateView(DashboardUpdateView):
    model = MaEquipment


class MaEquipmentDetailView(DashboardDetailView):
    model = MaEquipment
    fields = ['name', 'type']


''' Main Equipment Type Views '''


class MaEquipmentTypeListView(DashboardListView):
    model = MaEquipmentType
    fields = ['id', 'name']


class MaEquipmentTypeCreateView(DashboardCreateView):
    model = MaEquipmentType


class MaEquipmentTypeUpdateView(DashboardUpdateView):
    model = MaEquipmentType


class MaEquipmentTypeDetailView(DashboardDetailView):
    model = MaEquipmentType
    datatable_options = {
        'columns': ['name', 'type']
    }

''' Main Bank Views '''


class MaBankListView(DashboardListView):
    model = MaBank
    datatable_options = {
        'columns': [
            'id',
            'name',
            (_('Code'), 'number'),
        ],
        'searches': ['name', 'number']
    }

class MaBankCreateView(DashboardCreateView):
    model = MaBank
    success_url = reverse_lazy('main_bank')

class MaBankUpdateView(DashboardUpdateView):
    model = MaBank
    success_url = reverse_lazy('main_bank')

class MaBankDetailView(DashboardDetailView):
    model = MaBank
    fields = ['name', 'type']



''' Main Person Views '''
class MaPersonListView(DashboardListView):
    model = MaPerson
    fields = ['id', 'name', (_('Type'), 'get_type_icon'), (_('Ocupation'), 'get_ocupation_icon'), ]


class MaPersonCreateView(DashboardCreateView):
    model = MaPerson
    form_class = MaMultiPersonForm

    def get_success_url(self):
        return self.object.get_absolute_url()

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        bankformset = MaBankAccountFormset(request.POST)

        if form.is_valid() and bankformset.is_valid():
            return self.form_valid(form, bankformset)
        else:
            return self.form_invalid(form, bankformset)

    def form_valid(self, form, bankformset):
        self.object = form.save()
        bankformset.save()
        messages.success(self.request, _('Person') + ' ' + self.object.name + ' ' + _('created successfully'))
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, bankformset):
        return self.render_to_response(self.get_context_data(form=form, bankformset=bankformset))

    def get_context_data(self, **kwargs):
        context = super(MaPersonCreateView, self).get_context_data(**kwargs)
        context['bankformset'] = kwargs.get('bankformset', MaBankAccountFormset())

        return context


class MaPersonUpdateView(DashboardUpdateView):
    model = MaPerson
    form_class = MaMultiPersonForm

    def get_success_url(self):
        return self.object.get_absolute_url()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        bankformset = MaBankAccountFormset(request.POST, instance=self.object)

        if form.is_valid() and bankformset.is_valid():
            return self.form_valid(form, bankformset)
        else:
            return self.form_invalid(form, bankformset)

    def form_valid(self, form, bankformset):
        self.object = form.save()
        bankformset.save()
        messages.success(self.request, _('Person') + ' ' + self.object.name + ' ' + _('updated successfully'))
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, bankformset):
        return self.render_to_response(self.get_context_data(form=form, bankformset=bankformset))

    def get_context_data(self, **kwargs):
        context = super(MaPersonUpdateView, self).get_context_data(**kwargs)
        context['bankformset'] = kwargs.get('bankformset', MaBankAccountFormset(instance=self.object))

        return context


class MaPersonDetailView(DashboardDetailView):
    model = MaPerson
    fields = ['person__name', 'department']


'''Main Department Views'''


class MaDepartmentListView(DashboardListView):
    model = MaDepartment
    fields = ['id', 'name']

class MaDepartmentCreateView(DashboardCreateView):
    model = MaDepartment
    fields = ['name']
    success_url = reverse_lazy('main_department')

class MaDepartmentUpdateView(DashboardUpdateView):
    model = MaDepartment
    fields = ['name']
    success_url = reverse_lazy('main_department')


'''Main EmployeeFunction Views'''


class MaEmployeeFunctionListView(DashboardListView):
    model = MaEmployeeFunction
    fields = ['id', 'name']

class MaEmployeeFunctionCreateView(DashboardCreateView):
    model = MaEmployeeFunction
    fields = ['name', 'description']
    success_url = reverse_lazy('main_employee_function')

class MaEmployeeFunctionUpdateView(DashboardUpdateView):
    model = MaEmployeeFunction
    fields = ['name', 'description']
    success_url = reverse_lazy('main_employee_function')


'''Main Employee Views'''


class MaEmployeeListView(DashboardListView):
    model = MaEmployee
    fields = ['id', (_('Name'), 'get_name'), 'department']

class MaEmployeeDetailView(DashboardDetailView):
    model = MaEmployee
    fields = ['person__name', 'department']

class MaEmployeeCreateView(DashboardCreateView):
    model = MaEmployee
    form_class = MaEmployeeForm

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        second_form = MaPersonForm(request.POST, request.FILES)

        if form.is_valid() and second_form.is_valid():
            return self.form_valid(form, second_form)
        else:
            return self.form_invalid(form, second_form)

    def form_valid(self, form, second_form):
        second_form.instance.person_type = 'F'
        second_form.save()
        form.instance.person = second_form.instance
        self.object = form.save()
        messages.success(self.request, _('Employee created successfully'))
        return HttpResponseRedirect(form.instance.get_absolute_url())

    def form_invalid(self, form, second_form):
        return self.render_to_response(self.get_context_data(form=form, second_form=second_form))

    def get_context_data(self, **kwargs):
        context = super(MaEmployeeCreateView, self).get_context_data(**kwargs)
        context['second_form'] = kwargs.get('second_form', MaPersonForm())

        return context

class MaEmployeeUpdateView(DashboardUpdateView):
    model = MaEmployee
    form_class = MaEmployeeForm
    success_url = reverse_lazy('main_employee')


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        second_form = MaPersonForm(request.POST, request.FILES, instance=self.object.person)

        if form.is_valid() and second_form.is_valid():
            return self.form_valid(form, second_form)
        else:
            return self.form_invalid(form, second_form)

    def form_valid(self, form, second_form):
        second_form.save()
        form.instance.person = second_form.instance
        self.object = form.save()
        messages.success(self.request, _('Employee updated successfully!'))
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form, second_form):
        return self.render_to_response(self.get_context_data(form=form, second_form=second_form))

    def get_context_data(self, **kwargs):
        context = super(MaEmployeeUpdateView, self).get_context_data(**kwargs)
        context['second_form'] = kwargs.get('second_form', MaPersonForm(instance=self.object.person))

        return context


'''Main Customer/Supplier Views'''


class MaCustomerSupplierDetailView(DashboardDetailView):
    model = MaCustomerSupplier
    fields = ['id', 'person__name', 'type']

class MaCustomerSupplierListView(DashboardListView):
    model = MaCustomerSupplier
    fields = ['id', (_('Name'), 'person__name'), (_('Type'), 'get_type_icon')]

class MaCustomerSupplierCreateView(DashboardCreateView):
    model = MaCustomerSupplier
    form_class = MaCustomerSupplierForm

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        second_form = MaMultiPersonForm(request.POST, request.FILES)
        bankformset = MaBankAccountFormset(request.POST, request.FILES)

        if form.is_valid() and second_form.is_valid() and bankformset.is_valid():
            return self.form_valid(form, second_form, bankformset)
        else:
            return self.form_invalid(form, second_form, bankformset)

    def form_valid(self, form, second_form, bankformset):
        person = second_form.save()
        form.instance.person = person
        self.object = form.save()
        bankformset.save()
        messages.success(self.request, _('CustomerSupplier created successfully'))
        return HttpResponseRedirect(form.instance.get_absolute_url())

    def form_invalid(self, form, second_form, bankformset):
        return self.render_to_response(self.get_context_data(form=form, second_form=second_form,
                                                             bankformset=bankformset))

    def get_context_data(self, **kwargs):
        context = super(MaCustomerSupplierCreateView, self).get_context_data(**kwargs)
        context['second_form'] = kwargs.get('second_form', MaMultiPersonForm())
        context['bankformset'] = kwargs.get('bankformset', MaBankAccountFormset())

        return context

class MaCustomerSupplierUpdateView(DashboardUpdateView):
    model = MaCustomerSupplier
    form_class = MaCustomerSupplierForm
    success_url = reverse_lazy('main_customer_supplier')


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        second_form = MaMultiPersonForm(request.POST, request.FILES, instance=self.object.person)
        bankformset = MaBankAccountFormset(request.POST, instance=self.object.person)

        if form.is_valid() and second_form.is_valid() and bankformset.is_valid():
            return self.form_valid(form, second_form, bankformset)
        else:
            return self.form_invalid(form, second_form, bankformset)

    def form_valid(self, form, second_form, bankformset):
        person = second_form.save()
        form.instance.person = person
        self.object = form.save()
        bankformset.save()
        messages.success(self.request, _('CustomerSupplier updated successfully'))
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form, second_form, bankformset):
        return self.render_to_response(self.get_context_data(form=form, second_form=second_form, bankformset=bankformset))

    def get_context_data(self, **kwargs):
        context = super(MaCustomerSupplierUpdateView, self).get_context_data(**kwargs)
        context['second_form'] = kwargs.get('second_form', MaMultiPersonForm(instance=self.object.person))
        context['bankformset'] = kwargs.get('bankformset', MaBankAccountFormset(instance=self.object.person))

        return context