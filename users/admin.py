from django.contrib import admin
from .models import Users, EmployeeKPIs, PersonalGoals

admin.site.register(Users)
admin.site.register(EmployeeKPIs)
admin.site.register(PersonalGoals)