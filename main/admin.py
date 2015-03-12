from django.contrib import admin

# Register your models here.
from simple_history.admin import SimpleHistoryAdmin
from main.models import MaDepartment, MaEmployee, MaEmployeeFunction, MaPerson


class MaDepartmentAdmin(admin.ModelAdmin):
    model = MaDepartment

class MaEmployeeFunctionAdmin(SimpleHistoryAdmin):
    model = MaEmployeeFunction

class MaEmployeeAdmin(admin.ModelAdmin):
    model = MaEmployee

class MaPersonAdmin(SimpleHistoryAdmin):
    model = MaPerson


admin.site.register(MaDepartment, MaDepartmentAdmin)
admin.site.register(MaEmployee, MaEmployeeAdmin)
admin.site.register(MaEmployeeFunction, MaEmployeeFunctionAdmin)
admin.site.register(MaPerson, MaPersonAdmin)
