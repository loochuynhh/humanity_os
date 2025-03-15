from django.contrib import admin
from .models import Forms, FormQuestions, FormResponses

admin.site.register(Forms)
admin.site.register(FormQuestions)
admin.site.register(FormResponses)