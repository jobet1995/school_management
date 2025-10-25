import os
import django
from django.db import connection

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from cms_plugins.models import UpcomingEventsPlugin

def check_table_schema():
    # Get the table name
    table_name = UpcomingEventsPlugin._meta.db_table
    print(f"Checking table: {table_name}")
    
    # Check if the table exists and its columns
    with connection.cursor() as cursor:
        try:
            # For SQLite, we can use this query to get column info
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            print("Columns in table:")
            for column in columns:
                print(f"  - {column[1]} ({column[2]})")
        except Exception as e:
            print(f"Error checking table schema: {e}")

if __name__ == "__main__":
    check_table_schema()