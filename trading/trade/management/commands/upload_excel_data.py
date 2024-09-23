# management/commands/upload_excel_data.py
from django.core.management.base import BaseCommand
from .utils import upload_tick_excel_to_sql 

class Command(BaseCommand):
    help = "Upload data from Excel files to the database"

    def handle(self, *args, **kwargs):
        directory_path = '/workspaces/trading_project/trading/NiftyRaw2024Options' 
        upload_tick_excel_to_sql(directory_path)
        self.stdout.write(self.style.SUCCESS("Data uploaded successfully"))

