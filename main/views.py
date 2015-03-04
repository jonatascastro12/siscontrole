from django.contrib.messages.context_processors import messages
from django.core.urlresolvers import reverse_lazy

# Create your views here.
from django.http.response import HttpResponseRedirect
from django.utils.translation import ugettext as _
from main.forms import MaEmployeeForm, MaPersonForm
from main.models import MaDepartment, MaEmployee, MaEmployeeFunction
from siscontrole.views import DashboardCreateView, DashboardListView, DashboardDeleteView, \
    DashboardUpdateView


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
    fields = ['name']
    success_url = reverse_lazy('main_employee_function')

class MaEmployeeFunctionUpdateView(DashboardUpdateView):
    model = MaEmployeeFunction
    fields = ['name']
    success_url = reverse_lazy('main_employee_function')

class MaEmployeeFunctionDeleteView(DashboardDeleteView):
    success_url = reverse_lazy('main_employee_function')
    

'''Main Employee Views'''


class MaEmployeeListView(DashboardListView):
    model = MaEmployee
    fields = ['id', 'person__name', 'department']

class MaEmployeeCreateView(DashboardCreateView):
    model = MaEmployee
    form_class = MaEmployeeForm

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        employee_form = self.get_form(form_class)
        person_form = MaPersonForm(request.POST, request.FILES)

        if employee_form.is_valid() and person_form.is_valid():
            return self.form_valid(employee_form, person_form)
        else:
            return self.form_invalid(employee_form, person_form)

    def form_valid(self, form, person_form):
        person_form = MaPersonForm(self.request.POST, self.request.FILES)
        person_form.save()
        form.instance.person = person_form.instance
        self.object = form.save()
        messages.success(self.request, _('Employee created successfully'))
        return HttpResponseRedirect(form.instance.get_absolute_url())

    def form_invalid(self, form, person_form):
        return self.render_to_response(self.get_context_data(form=form, person_form=person_form))

    def get_context_data(self, **kwargs):
        context = super(MaEmployeeCreateView, self).get_context_data(**kwargs)
        context['person_form'] = kwargs.get('person_form', MaPersonForm())

        return context

class MaEmployeeUpdateView(DashboardUpdateView):
    model = MaEmployee
    form_class = MaEmployeeForm
    success_url = reverse_lazy('main_employee')

class MaEmployeeDeleteView(DashboardDeleteView):
    success_url = reverse_lazy('main_department')