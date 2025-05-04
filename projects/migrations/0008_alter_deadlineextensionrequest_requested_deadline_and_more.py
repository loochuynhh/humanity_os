# projects/migrations/0008_auto_20250427_xxxx.py
from django.db import migrations, models
from django.utils import timezone


def convert_date_to_datetime(apps, schema_editor):
    # Lấy các model lịch sử
    Projects = apps.get_model('projects', 'Projects')
    Tasks = apps.get_model('projects', 'Tasks')
    DeadlineExtensionRequest = apps.get_model('projects', 'DeadlineExtensionRequest')
    TeamProjectMembership = apps.get_model('projects', 'TeamProjectMembership')

    # Chuyển đổi cho Projects
    for project in Projects.objects.all():
        project.start_date = timezone.make_aware(
            timezone.datetime.combine(project.start_date, timezone.datetime.min.time())
        )
        project.end_date = timezone.make_aware(
            timezone.datetime.combine(project.end_date, timezone.datetime.min.time())
        )
        project.save()

    # Chuyển đổi cho Tasks
    for task in Tasks.objects.all():
        task.deadline = timezone.make_aware(
            timezone.datetime.combine(task.deadline, timezone.datetime.min.time())
        )
        if task.start_date:
            task.start_date = timezone.make_aware(
                timezone.datetime.combine(task.start_date, timezone.datetime.min.time())
            )
        if task.completed_date:
            task.completed_date = timezone.make_aware(
                timezone.datetime.combine(task.completed_date, timezone.datetime.min.time())
            )
        task.save()

    # Chuyển đổi cho DeadlineExtensionRequest
    for request in DeadlineExtensionRequest.objects.all():
        request.requested_deadline = timezone.make_aware(
            timezone.datetime.combine(request.requested_deadline, timezone.datetime.min.time())
        )
        request.save()

    # Chuyển đổi cho TeamProjectMembership
    for membership in TeamProjectMembership.objects.all():
        membership.join_date = timezone.make_aware(
            timezone.datetime.combine(membership.join_date, timezone.datetime.min.time())
        )
        membership.save()


def reverse_convert_datetime_to_date(apps, schema_editor):
    # Hàm đảo ngược để hỗ trợ rollback (nếu cần)
    Projects = apps.get_model('projects', 'Projects')
    Tasks = apps.get_model('projects', 'Tasks')
    DeadlineExtensionRequest = apps.get_model('projects', 'DeadlineExtensionRequest')
    TeamProjectMembership = apps.get_model('projects', 'TeamProjectMembership')

    for project in Projects.objects.all():
        project.start_date = project.start_date.date()
        project.end_date = project.end_date.date()
        project.save()

    for task in Tasks.objects.all():
        task.deadline = task.deadline.date()
        if task.start_date:
            task.start_date = task.start_date.date()
        if task.completed_date:
            task.completed_date = task.completed_date.date()
        task.save()

    for request in DeadlineExtensionRequest.objects.all():
        request.requested_deadline = request.requested_deadline.date()
        request.save()

    for membership in TeamProjectMembership.objects.all():
        membership.join_date = membership.join_date.date()
        membership.save()


class Migration(migrations.Migration):
    dependencies = [
        ('projects', '0007_taskassignments_status'),
    ]

    operations = [
        migrations.RunPython(convert_date_to_datetime, reverse_convert_datetime_to_date),
        migrations.AlterField(
            model_name='Projects',
            name='start_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='Projects',
            name='end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='Tasks',
            name='deadline',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='Tasks',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='Tasks',
            name='completed_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='DeadlineExtensionRequest',
            name='requested_deadline',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='TeamProjectMembership',
            name='join_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]