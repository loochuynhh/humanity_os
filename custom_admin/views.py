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
from custom_admin.utils import superuser_required, get_app_list
from django.contrib import messages
from django.apps import apps
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.admin.models import LogEntry
from django.urls import reverse


@superuser_required
def index(request):
    return render(request, "pages/index.html", {"segment": "dashboard"})


# Authentication
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
    Global search functionality across permitted models with enhanced logic
    """
    query = request.GET.get('q', '').strip()
    results = []
    max_results_per_model = 5
    total_max_results = 50
    
    if query:
        # Get permitted models from get_app_list
        app_list = get_app_list({'request': request, 'user': request.user})
        result_count = 0
        
        for app in app_list:
            for model_dict in app['models']:
                model = apps.get_model(app['app_label'], model_dict['model_name'])
                model_admin = admin.site._registry.get(model)
                
                if not model_admin:
                    continue
                
                # Check permissions
                if not model_admin.has_module_permission(request):
                    continue
                
                perms = model_admin.get_model_perms(request)
                if not (perms.get('change', False) or perms.get('view', False)):
                    continue
                
                # Get searchable fields (prioritize 'name', 'title', 'description')
                search_fields = []
                priority_fields = ['name', 'title', 'description']
                other_fields = []
                
                for field in model._meta.fields:
                    field_type = field.get_internal_type()
                    if field_type in ['CharField', 'TextField', 'EmailField', 'SlugField']:
                        if field.name in priority_fields:
                            search_fields.append(field.name)
                        else:
                            other_fields.append(field.name)
                
                # Combine fields: priority first, then others
                search_fields.extend(other_fields)
                
                if search_fields:
                    try:
                        # Build Q objects for search
                        q_objects = Q()
                        for field in search_fields:
                            q_objects |= Q(**{f"{field}__icontains": query})
                        
                        # Get matching objects
                        queryset = model_admin.get_queryset(request).filter(q_objects)
                        
                        # Handle related fields (e.g., project name in Task)
                        if model._meta.model_name == 'task':
                            try:
                                queryset |= model_admin.get_queryset(request).filter(
                                    project__name__icontains=query
                                )
                            except:
                                pass
                        
                        # Limit results and remove duplicates
                        matching_objects = queryset.distinct()[:max_results_per_model]
                        
                        if matching_objects and result_count < total_max_results:
                            objects = []
                            for obj in matching_objects:
                                # Get admin change URL
                                try:
                                    url = reverse(
                                        f'admin:{model._meta.app_label}_{model._meta.model_name}_change',
                                        args=[obj.pk]
                                    )
                                except:
                                    url = None
                                
                                # Get matched field value (for display)
                                matched_value = None
                                for field in search_fields:
                                    value = getattr(obj, field, None)
                                    if value and query.lower() in str(value).lower():
                                        matched_value = str(value)[:100]
                                        break
                                
                                objects.append({
                                    'id': obj.pk,
                                    'name': str(obj),
                                    'url': url,
                                    'matched_value': matched_value,
                                })
                            
                            results.append({
                                'model_name': model._meta.verbose_name,
                                'model_name_plural': model._meta.verbose_name_plural,
                                'app_label': model._meta.app_label,
                                'model': model._meta.model_name,
                                'objects': objects,
                            })
                            result_count += len(objects)
                            
                            if result_count >= total_max_results:
                                break
                    except Exception as e:
                        messages.error(request, f"Lỗi khi tìm kiếm trong {model._meta.verbose_name_plural}: {str(e)}")
                
                if result_count >= total_max_results:
                    break
    
    return render(request, 'admin/search_results.html', {
        'query': query,
        'results': results,
    })