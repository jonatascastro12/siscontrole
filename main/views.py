from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.utils.translation import ugettext as _
from main.forms import MaEmployeeForm, MaPersonForm, MaCustomerSupplierForm, MaMultiPersonForm, MaBankAccountFormset
from main.models import MaDepartment, MaEmployee, MaEmployeeFunction, MaCustomerSupplier
from siscontrole.views import DashboardCreateView, DashboardListView, DashboardDeleteView, \
    DashboardUpdateView, DashboardDetailView


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

class MaDepartmentDeleteView(DashboardDeleteView):
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

class MaEmployeeFunctionDeleteView(DashboardDeleteView):
    success_url = reverse_lazy('main_employee_function')
    

'''Main Employee Views'''


class MaEmployeeListView(DashboardListView):
    model = MaEmployee
    fields = ['id', 'person__name', 'department']

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
        second_form = MaPersonForm(self.request.POST, self.request.FILES)
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

class MaEmployeeDeleteView(DashboardDeleteView):
    success_url = reverse_lazy('main_department')


'''Main Customer/Supplier Views'''


class MaCustomerSupplierDetailView(DashboardDetailView):
    model = MaCustomerSupplier
    fields = ['id', 'person__name', 'type']

class MaCustomerSupplierListView(DashboardListView):
    model = MaCustomerSupplier
    fields = ['id', 'person__name', 'type']

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
        bankformset = MaBankAccountFormset(request.POST, instance=self.object)

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
        context['bankformset'] = kwargs.get('bankformset', MaBankAccountFormset(instance=self.object))

        return context

class MaCustomerSupplierDeleteView(DashboardDeleteView):
    success_url = reverse_lazy('main_department')