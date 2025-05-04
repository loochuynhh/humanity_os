# kpis/migrations/0003_kpis_employeekpis_changes.py
from django.db import migrations, models
import django.db.models.deletion
from django.utils import timezone
from datetime import datetime, timedelta
import logging

# Set up logging
logger = logging.getLogger(__name__)

def migrate_kpi_data(apps, schema_editor):
    KPIs = apps.get_model('kpis', 'KPIs')
    EmployeeKPIs = apps.get_model('kpis', 'EmployeeKPIs')

    # Add default unit, kpi_type, and weight to KPIs
    for kpi in KPIs.objects.all():
        kpi.unit = ''  # Default unit
        kpi.kpi_type = 'Quantitative'  # Default type
        kpi.weight = 1.0
        kpi.save()
        logger.info(f"Updated KPI: {kpi.name}, type: {kpi.kpi_type}, unit: {kpi.unit}, weight: {kpi.weight}")

    # Migrate EmployeeKPIs data
    for emp_kpi in EmployeeKPIs.objects.all():
        # Convert target_value and actual_value to FloatField
        try:
            emp_kpi.target_value = float(emp_kpi.target_value or 0)
        except (ValueError, TypeError):
            emp_kpi.target_value = 0.0
            logger.warning(f"Invalid target_value for EmployeeKPI {emp_kpi.id}, set to 0.0")
        try:
            emp_kpi.actual_value = float(emp_kpi.actual_value) if emp_kpi.actual_value else None
        except (ValueError, TypeError):
            emp_kpi.actual_value = None
            logger.warning(f"Invalid actual_value for EmployeeKPI {emp_kpi.id}, set to None")

        # Set achieved_percentage
        emp_kpi.achieved_percentage = 0.0

        # Set start_date and end_date based on time_period
        now = timezone.now()
        time_period = (emp_kpi.time_period or '').lower().strip()
        if time_period in ['week', 'weekly']:
            emp_kpi.time_period = 'Weekly'
            emp_kpi.start_date = now - timedelta(days=now.weekday())  # Start of current week
            emp_kpi.end_date = emp_kpi.start_date + timedelta(days=6)  # End of week
        elif time_period in ['month', 'monthly']:
            emp_kpi.time_period = 'Monthly'
            emp_kpi.start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)  # Start of month
            # Calculate end of month
            next_month = (emp_kpi.start_date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
            emp_kpi.end_date = next_month.replace(hour=23, minute=59, second=59, microsecond=999999)
        elif time_period in ['quarter', 'quarterly']:
            emp_kpi.time_period = 'Quarterly'
            quarter_start_month = ((now.month - 1) // 3) * 3 + 1
            emp_kpi.start_date = now.replace(month=quarter_start_month, day=1, hour=0, minute=0, second=0, microsecond=0)
            quarter_end_month = quarter_start_month + 2
            emp_kpi.end_date = now.replace(month=quarter_end_month, day=28) + timedelta(days=4)
            emp_kpi.end_date = emp_kpi.end_date.replace(day=1, hour=23, minute=59, second=59, microsecond=999999) - timedelta(days=1)
        elif time_period in ['year', 'yearly']:
            emp_kpi.time_period = 'Yearly'
            emp_kpi.start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            emp_kpi.end_date = now.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
        else:
            emp_kpi.time_period = 'Monthly'  # Default
            emp_kpi.start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            next_month = (emp_kpi.start_date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
            emp_kpi.end_date = next_month.replace(hour=23, minute=59, second=59, microsecond=999999)
            logger.warning(f"Invalid time_period '{time_period}' for EmployeeKPI {emp_kpi.id}, set to Monthly")

        # Ensure end_date >= start_date
        if emp_kpi.end_date < emp_kpi.start_date:
            emp_kpi.end_date = emp_kpi.start_date + timedelta(days=30)
            logger.warning(f"Adjusted end_date for EmployeeKPI {emp_kpi.id} to {emp_kpi.end_date}")

        emp_kpi.save()
        logger.info(f"Updated EmployeeKPI {emp_kpi.id}: target={emp_kpi.target_value}, actual={emp_kpi.actual_value}, "
                    f"start_date={emp_kpi.start_date}, end_date={emp_kpi.end_date}, period={emp_kpi.time_period}")


class Migration(migrations.Migration):
    dependencies = [
        ('kpis', '0002_initial'),
        ('projects', '0008_alter_deadlineextensionrequest_requested_deadline_and_more'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(migrate_kpi_data, reverse_code=migrations.RunPython.noop),
        migrations.AddField(
            model_name='KPIs',
            name='kpi_type',
            field=models.CharField(choices=[('Quantitative', 'Quantitative'), ('Qualitative', 'Qualitative'), ('Efficiency', 'Efficiency'), ('Quality', 'Quality')], default='Quantitative', max_length=20),
        ),
        migrations.AddField(
            model_name='KPIs',
            name='project',
            field=models.ForeignKey(blank=True, help_text='Optional: Link to a specific project', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kpis', to='projects.projects'),
        ),
        migrations.AddField(
            model_name='KPIs',
            name='unit',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='KPIs',
            name='weight',
            field=models.FloatField(default=1.0, help_text='Weight for overall performance calculation'),
        ),
        migrations.AlterField(
            model_name='EmployeeKPIs',
            name='evaluation',
            field=models.CharField(blank=True, choices=[('Exceeded', 'Exceeded'), ('Achieved', 'Achieved'), ('Partially Achieved', 'Partially Achieved'), ('Not Achieved', 'Not Achieved')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='EmployeeKPIs',
            name='time_period',
            field=models.CharField(choices=[('Weekly', 'Weekly'), ('Monthly', 'Monthly'), ('Quarterly', 'Quarterly'), ('Yearly', 'Yearly')], default='Monthly', max_length=20),
        ),
        migrations.AlterField(
            model_name='EmployeeKPIs',
            name='target_value',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='EmployeeKPIs',
            name='actual_value',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='EmployeeKPIs',
            name='achieved_percentage',
            field=models.FloatField(default=0.0, help_text='Percentage of target achieved'),
        ),
        migrations.AddField(
            model_name='EmployeeKPIs',
            name='start_date',
            field=models.DateTimeField(default=timezone.now),
        ),
        migrations.AddField(
            model_name='EmployeeKPIs',
            name='end_date',
            field=models.DateTimeField(default=timezone.now() + timezone.timedelta(days=30)),
        ),
        migrations.AddField(
            model_name='EmployeeKPIs',
            name='task',
            field=models.ForeignKey(blank=True, help_text='Optional: Link to a specific task', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kpis', to='projects.tasks'),
        ),
        migrations.AddIndex(
            model_name='EmployeeKPIs',
            index=models.Index(fields=['user', 'start_date'], name='employee_kpis_user_start_date_idx'),
        ),
        migrations.AddIndex(
            model_name='EmployeeKPIs',
            index=models.Index(fields=['kpi', 'time_period'], name='employee_kpis_kpi_period_idx'),
        ),
    ]