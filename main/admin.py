from django.contrib import admin

# Register your models here.
from main.models import MaDepartment, MaEmployee, MaEmployeeFunction, MaPerson


class MaDepartmentAdmin(admin.ModelAdmin):
    model = MaDepartment

class MaEmployeeFunctionAdmin(admin.ModelAdmin):
    model = MaEmployeeFunction

class MaEmployeeAdmin(admin.ModelAdmin):
    model = MaEmployee

class MaPersonAdmin(admin.ModelAdmin):
    model = MaPerson


admin.site.register(MaDepartment, MaDepartmentAdmin)
admin.site.register(MaEmployee, MaEmployeeAdmin)
admin.site.register(MaEmployeeFunction, MaEmployeeFunctionAdmin)
admin.site.register(MaPerson, MaPersonAdmin)
