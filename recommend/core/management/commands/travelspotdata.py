import csv
from django.core.management.base import BaseCommand
from travels.models import TravelSpot

class Command(BaseCommand):
    help = "This command creates classification code"

    def handle(self, *args, **options):
        f = open('csv/travelspot_data.csv', 'r', encoding='utf-8')
        reader = csv.reader(f)
        for row in reader:
            areacode,cat1,cat2,content_id,content_type,mapx,mapy,readcount,title = row            
            TravelSpot.objects.create(
        	    areacode = areacode,
                cat1 = cat1,
                cat2 = cat2,
                content_id = content_id,
                content_type = content_type,
                mapx = mapx,
                mapy = mapy,
                readcount = readcount,
                title = title
            )
        f.close()

        self.stdout.write(self.style.SUCCESS(f"created!"))