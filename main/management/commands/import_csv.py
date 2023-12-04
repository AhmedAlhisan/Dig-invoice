import csv
from django.core.management.base import BaseCommand
from main.models import DepartmentBudget  # Adjust the import according to your project structure
from datetime import datetime

class Command(BaseCommand):
    help = 'Import a CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The CSV file to import')

    def handle(self, *args, **kwargs):
        file_path = kwargs['csv_file']

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                # Convert date from string to date object
               

                DepartmentBudget.objects.create(
                    department_name=row['Department Name'],
                    budget=row['Budget'],
                    available_budget=row['AvailableBudget'],
                   
                )

        self.stdout.write(self.style.SUCCESS('Successfully imported CSV file'))
