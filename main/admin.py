from django.contrib import admin

# Register your models here.
from main.models import MaDepartment


class MaDepartmentAdmin(admin.ModelAdmin):
    model = MaDepartment


admin.site.register(MaDepartment, MaDepartmentAdmin)
