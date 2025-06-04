from django.contrib import admin
from .models import Projects, Tasks, TaskAssignments, TimeEntries, DeadlineExtensionRequest, TeamProjectMembership

class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'manager')
    # Giữ nguyên quyền mặc định (đầy đủ CRUD)

class TasksAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'deadline', 'status', 'difficulty')
    # Giữ nguyên quyền mặc định (đầy đủ CRUD)

class TaskAssignmentsAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'role', 'status')
    # Giữ nguyên quyền mặc định (đầy đủ CRUD)

class TimeEntriesAdmin(admin.ModelAdmin):
    list_display = ('task_assignment', 'start_time', 'end_time', 'duration')
    list_filter = ('start_time',)
    search_fields = ('task_assignment__task__title', 'task_assignment__user__username')
    
    # Vô hiệu hóa quyền thêm, xóa và chỉnh sửa
    def has_add_permission(self, request):
        return False
        
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

class DeadlineExtensionRequestAdmin(admin.ModelAdmin):
    list_display = ('task', 'requested_by', 'requested_deadline', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('task__title', 'requested_by__username', 'reason')
    
    # Vô hiệu hóa quyền thêm và xóa
    def has_add_permission(self, request):
        return False
        
    def has_delete_permission(self, request, obj=None):
        return False
    
    # Chỉ cho phép chỉnh sửa trường status
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [f.name for f in obj._meta.fields if f.name != 'status']
        return []

class TeamProjectMembershipAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'join_date', 'role')
    # Giữ nguyên quyền mặc định (đầy đủ CRUD)

admin.site.register(Projects, ProjectsAdmin)
admin.site.register(Tasks, TasksAdmin)
admin.site.register(TaskAssignments, TaskAssignmentsAdmin)
admin.site.register(TimeEntries, TimeEntriesAdmin)
admin.site.register(DeadlineExtensionRequest, DeadlineExtensionRequestAdmin)
admin.site.register(TeamProjectMembership, TeamProjectMembershipAdmin)
