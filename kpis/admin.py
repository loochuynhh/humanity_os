from django.contrib import admin
from .models import KPIs, EmployeeKPIs

class KPIsAdmin(admin.ModelAdmin):
    list_display = ('name', 'kpi_type', 'weight', 'project')

class EmployeeKPIsAdmin(admin.ModelAdmin):
    list_display = ('user', 'kpi', 'target_value', 'actual_value', 'achieved_percentage', 'evaluation', 'time_period')
    list_filter = ('time_period', 'evaluation')
    search_fields = ('user__username', 'kpi__name')
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [f.name for f in obj._meta.fields if f.name not in ['target_value', 'evaluation']]
        return []

admin.site.register(KPIs, KPIsAdmin)
admin.site.register(EmployeeKPIs, EmployeeKPIsAdmin)
