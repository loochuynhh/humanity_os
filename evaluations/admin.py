from django.contrib import admin
from .models import Forms, FormQuestions, FormResponses

class FormsAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'period', 'deadline', 'status')
    # Giữ nguyên quyền mặc định (đầy đủ CRUD)

class FormQuestionsAdmin(admin.ModelAdmin):
    list_display = ('form', 'question_text', 'question_type', 'max_score')
    # Giữ nguyên quyền mặc định (đầy đủ CRUD)

class FormResponsesAdmin(admin.ModelAdmin):
    list_display = ('form', 'question', 'user', 'target_user', 'answer_type', 'created_at')
    list_filter = ('answer_type', 'created_at', 'form')
    search_fields = ('user__username', 'target_user__username', 'form__name', 'answer')
    
    # Vô hiệu hóa quyền thêm, xóa và chỉnh sửa
    def has_add_permission(self, request):
        return False
        
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(Forms, FormsAdmin)
admin.site.register(FormQuestions, FormQuestionsAdmin)
admin.site.register(FormResponses, FormResponsesAdmin)
