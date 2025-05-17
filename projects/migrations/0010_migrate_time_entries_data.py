# Generated manually

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_taskassignments_role_taskassignments_actual_time_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            # Di chuyển dữ liệu từ bảng time_entries cũ sang time_entries_new
            """
            INSERT INTO time_entries_new (task_assignment_id, start_time, end_time, duration)
            SELECT ta.id, te.start_time, te.end_time, te.duration
            FROM time_entries te
            JOIN task_assignments ta ON te.task_id = ta.task_id AND te.user_id = ta.user_id
            WHERE ta.role = 'Thực hiện chính';
            """,
            # Reverse SQL (không thể khôi phục dữ liệu)
            "SELECT 1;"
        ),
        migrations.RunSQL(
            # Đổi tên bảng time_entries_new thành time_entries
            """
            DROP TABLE IF EXISTS time_entries;
            ALTER TABLE time_entries_new RENAME TO time_entries;
            """,
            # Reverse SQL (không thể khôi phục)
            "SELECT 1;"
        ),
    ]