from django.contrib import admin
from .models import Projects, Tasks, TaskAssignments, TimeEntries

admin.site.register(Projects)
admin.site.register(Tasks)
admin.site.register(TaskAssignments)
admin.site.register(TimeEntries)
