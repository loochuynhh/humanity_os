# Generated manually

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_alter_deadlineextensionrequest_requested_deadline_and_more'),
    ]

    operations = [
        # Thêm trường role vào TaskAssignments
        migrations.AddField(
            model_name='taskassignments',
            name='role',
            field=models.CharField(choices=[('Thực hiện chính', 'Thực hiện chính'), ('Đồng thực hiện', 'Đồng thực hiện'), ('Review', 'Review'), ('Test', 'Test'), ('Khác', 'Khác')], default='Thực hiện chính', max_length=50),
        ),
        
        # Thêm trường actual_time vào TaskAssignments
        migrations.AddField(
            model_name='taskassignments',
            name='actual_time',
            field=models.FloatField(default=0.0),
        ),
        
        # Thêm trường role vào TeamProjectMembership
        migrations.AddField(
            model_name='teamprojectmembership',
            name='role',
            field=models.CharField(default='Member', max_length=50),
        ),
        
        # Thêm chỉ mục cho TaskAssignments
        migrations.AddIndex(
            model_name='taskassignments',
            index=models.Index(fields=['task', 'user'], name='task_assignments_task_id_user_id_idx'),
        ),
        migrations.AddIndex(
            model_name='taskassignments',
            index=models.Index(fields=['status'], name='task_assignments_status_idx'),
        ),
        
        # Thêm chỉ mục cho DeadlineExtensionRequest
        migrations.AddIndex(
            model_name='deadlineextensionrequest',
            index=models.Index(fields=['task', 'status'], name='deadline_extension_requests_task_status_idx'),
        ),
        migrations.AddIndex(
            model_name='deadlineextensionrequest',
            index=models.Index(fields=['requested_by', 'status'], name='deadline_extension_requests_user_status_idx'),
        ),
        
        # Cập nhật ràng buộc unique_together cho TaskAssignments
        migrations.AlterUniqueTogether(
            name='taskassignments',
            unique_together={('task', 'user', 'role')},
        ),
        
        # Tạo bảng TimeEntries mới với liên kết đến TaskAssignment
        migrations.CreateModel(
            name='TimeEntriesNew',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('duration', models.FloatField(blank=True, null=True)),
                ('task_assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_entries', to='projects.taskassignments')),
            ],
            options={
                'verbose_name': 'Time Entry',
                'verbose_name_plural': 'Time Entries',
                'db_table': 'time_entries_new',
            },
        ),
        
        # Thêm chỉ mục cho TimeEntriesNew
        migrations.AddIndex(
            model_name='timeentriesnew',
            index=models.Index(fields=['task_assignment', 'start_time'], name='time_entries_new_task_assignment_start_time_idx'),
        ),
        migrations.AddIndex(
            model_name='timeentriesnew',
            index=models.Index(fields=['start_time'], name='time_entries_new_start_time_idx'),
        ),
        
        # Thêm verbose_name cho các model
        migrations.AlterModelOptions(
            name='projects',
            options={'verbose_name': 'Project', 'verbose_name_plural': 'Projects'},
        ),
        migrations.AlterModelOptions(
            name='tasks',
            options={'verbose_name': 'Task', 'verbose_name_plural': 'Tasks'},
        ),
        migrations.AlterModelOptions(
            name='taskassignments',
            options={'verbose_name': 'Task Assignment', 'verbose_name_plural': 'Task Assignments'},
        ),
        migrations.AlterModelOptions(
            name='deadlineextensionrequest',
            options={'verbose_name': 'Deadline Extension Request', 'verbose_name_plural': 'Deadline Extension Requests'},
        ),
        migrations.AlterModelOptions(
            name='teamprojectmembership',
            options={'verbose_name': 'Team Project Membership', 'verbose_name_plural': 'Team Project Memberships'},
        ),
    ] 