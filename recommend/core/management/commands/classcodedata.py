import csv
from django.core.management.base import BaseCommand
from travels.models import ClassificationCode

class Command(BaseCommand):
    help = "This command creates classification code"

    def handle(self, *args, **options):
        f = open('csv/classification_code.csv', 'r', encoding='utf-8')
        reader = csv.reader(f)
        for row in reader:
            contenttypeid,cat1,cat1_name,cat2,cat2_name = row            
            ClassificationCode.objects.create(
        	    contenttypeid = contenttypeid,
                cat1 = cat1,
                cat1_name = cat1_name,
                cat2 = cat2,
                cat2_name = cat2_name,
            )
        f.close()

        self.stdout.write(self.style.SUCCESS(f"created!"))