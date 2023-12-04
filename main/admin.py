from django.contrib import admin

# Register your models here.
from . models import DepartmentBudget ,Invoice

# Register your models here.

admin.site.register(DepartmentBudget)
admin.site.register(Invoice)
