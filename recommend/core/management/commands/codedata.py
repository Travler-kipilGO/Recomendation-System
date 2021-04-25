import csv
from django.core.management.base import BaseCommand
from travels.models import CodeData

class Command(BaseCommand):

    help = "This command creates code"

    def handle(self, *args, **options):
        f = open('csv/code_data.csv', 'r', encoding='utf-8')
        reader = csv.reader(f)
        for row in reader:
            code_id, code_info, code_from = row            
            CodeData.objects.create(
        	    code_id = code_id,
                code_info = code_info,
                code_from = code_from,
            )
        f.close()

        self.stdout.write(self.style.SUCCESS(f"created!"))