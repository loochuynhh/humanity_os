#!/usr/bin/env python
"""
Script để thực hiện migration và seed dữ liệu cho ứng dụng projects.
"""

import os
import sys
import django
from django.db import connection
from pathlib import Path

# Thêm thư mục gốc của dự án vào sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))

# Cấu hình Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "humanity_os.settings")
django.setup()

def execute_sql_file(file_path):
    """Thực hiện các câu lệnh SQL từ file."""
    print(f"Đang thực hiện file SQL: {file_path}")
    with open(file_path, 'r') as f:
        sql = f.read()
    
    with connection.cursor() as cursor:
        # Chia các câu lệnh SQL theo dấu chấm phẩy
        for statement in sql.split(';'):
            statement = statement.strip()
            if statement:
                print(f"Đang thực hiện: {statement[:50]}...")
                cursor.execute(statement)
    
    print("Hoàn thành thực hiện file SQL.")

def migrate_database():
    """Thực hiện migration."""
    print("Đang thực hiện migration...")
    
    # Thực hiện migration
    from django.core.management import call_command
    call_command('migrate', 'projects')
    
    print("Hoàn thành migration.")

def seed_database():
    """Seed dữ liệu mẫu."""
    print("Đang seed dữ liệu mẫu...")
    
    # Đường dẫn đến file SQL seed
    sql_file = os.path.join(BASE_DIR, 'projects', 'scripts', 'clear_and_seed_data.sql')
    execute_sql_file(sql_file)
    
    print("Hoàn thành seed dữ liệu mẫu.")

def migrate_time_entries():
    """Di chuyển dữ liệu từ bảng time_entries cũ sang time_entries_new."""
    print("Đang di chuyển dữ liệu từ time_entries sang time_entries_new...")
    
    sql = """
    INSERT INTO time_entries_new (task_assignment_id, start_time, end_time, duration)
    SELECT ta.id, te.start_time, te.end_time, te.duration
    FROM time_entries te
    JOIN task_assignments ta ON te.task_id = ta.task_id AND te.user_id = ta.user_id
    WHERE ta.role = 'Thực hiện chính';
    """
    
    with connection.cursor() as cursor:
        cursor.execute(sql)
    
    print("Hoàn thành di chuyển dữ liệu.")

def rename_time_entries_table():
    """Đổi tên bảng time_entries_new thành time_entries."""
    print("Đang đổi tên bảng time_entries_new thành time_entries...")
    
    sql = """
    DROP TABLE IF EXISTS time_entries;
    ALTER TABLE time_entries_new RENAME TO time_entries;
    """
    
    with connection.cursor() as cursor:
        for statement in sql.split(';'):
            statement = statement.strip()
            if statement:
                cursor.execute(statement)
    
    print("Hoàn thành đổi tên bảng.")

def main():
    """Hàm chính."""
    print("Bắt đầu quá trình migration và seed dữ liệu...")
    
    migrate_database()
    seed_database()
    migrate_time_entries()
    rename_time_entries_table()
    
    print("Hoàn thành quá trình migration và seed dữ liệu.")

if __name__ == "__main__":
    main() 