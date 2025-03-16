from django.contrib import admin
from .models import Company, Teams, TeamMembers

admin.site.register(Company)
admin.site.register(Teams)
admin.site.register(TeamMembers)
