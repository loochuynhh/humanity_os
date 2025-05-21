from django.shortcuts import render, redirect
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordChangeView,
    PasswordResetConfirmView,
)
from custom_admin.forms import (
    RegistrationForm,
    LoginForm,
    UserPasswordResetForm,
    UserSetPasswordForm,
    UserPasswordChangeForm,
)
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from custom_admin.utils import superuser_required
from django.contrib import messages
from django.apps import apps
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.admin.models import LogEntry


@superuser_required
def index(request):
    return render(request, "pages/index.html", {"segment": "dashboard"})

# Authenticatio
def logout_view(request):
    logout(request)
    return redirect("/admin/")


@login_required
@require_POST
def update_fixed_location(request):
    """
    Cập nhật vị trí cố định của người dùng.
    """
    try:
        fixed_location = request.POST.get('fixed_location', '')

        # Kiểm tra định dạng
        if fixed_location:
            try:
                lat, lng = map(float, fixed_location.split(','))
                if not (-90 <= lat <= 90 and -180 <= lng <= 180):
                    messages.error(request, "Vị trí không hợp lệ. Vui lòng kiểm tra lại.")
                    return redirect('profile')
            except:
                messages.error(request, "Định dạng vị trí không hợp lệ. Vui lòng sử dụng định dạng: latitude,longitude")
                return redirect('profile')

        # Cập nhật vị trí
        user = request.user
        user.fixed_location = fixed_location
        user.save()

        messages.success(request, "Cập nhật vị trí làm việc thành công.")
        return redirect('profile')
    except Exception as e:
        messages.error(request, f"Lỗi khi cập nhật vị trí: {str(e)}")
        return redirect('profile')


@staff_member_required
def index(request):
    """
    Admin index view with dashboard statistics
    """
    User = get_user_model()
    
    # Get counts for dashboard stats
    user_count = User.objects.count()
    
    # Try to get project count if the model exists
    project_count = 0
    try:
        Project = apps.get_model('projects', 'Project')
        project_count = Project.objects.count()
    except LookupError:
        pass
    
    # Try to get task count if the model exists
    task_count = 0
    try:
        Task = apps.get_model('projects', 'Task')
        task_count = Task.objects.count()
    except LookupError:
        pass
    
    # Get recent activity logs
    recent_logs = LogEntry.objects.select_related('content_type', 'user').order_by('-action_time')[:10]
    
    context = {
        'user_count': user_count,
        'project_count': project_count,
        'task_count': task_count,
        'activity_count': LogEntry.objects.count(),
        'recent_logs': recent_logs,
    }
    
    return render(request, 'admin/index.html', context)

@staff_member_required
def search(request):
    """
    Global search functionality across all models
    """
    query = request.GET.get('q', '')
    results = []
    
    if query:
        # Get all models
        all_models = apps.get_models()
        
        for model in all_models:
            # Skip some built-in models
            if model._meta.app_label in ['admin', 'contenttypes', 'sessions']:
                continue
            
            # Skip auth models we don't want to show
            if model._meta.app_label == 'auth' and model._meta.model_name in ['permission', 'group']:
                continue
            
            # Get searchable fields (text fields)
            search_fields = []
            for field in model._meta.fields:
                if field.get_internal_type() in ['CharField', 'TextField', 'EmailField', 'SlugField']:
                    search_fields.append(field.name)
            
            if search_fields:
                # Build Q objects for each search field
                q_objects = Q()
                for field in search_fields:
                    q_objects |= Q(**{f"{field}__icontains": query})
                
                # Get matching objects
                matching_objects = model.objects.filter(q_objects)[:10]
                
                if matching_objects:
                    results.append({
                        'model_name': model._meta.verbose_name,
                        'model_name_plural': model._meta.verbose_name_plural,
                        'app_label': model._meta.app_label,
                        'model': model._meta.model_name,
                        'objects': matching_objects,
                    })
    
    return render(request, 'admin/search_results.html', {
        'query': query,
        'results': results,
    })

