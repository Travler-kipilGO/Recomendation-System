from django.core.management.base import BaseCommand
from accommodations.models import Accommodation, Photo
from rooms.models import Room
from regions.models import Country, City
from core import crawler
import time
import re

class Command(BaseCommand):

    help = "This command creates data"


    def add_arguments(self, parser):
        parser.add_argument(
            "--keyword", help="keyword"
        )

    def handle(self, *args, **options):
        try:
            country = Country.objects.get(name='대한민국')
        except:
            country = Country.objects.create(name='대한민국')

        keyword = options.get("keyword")
        try:
            city = City.objects.get(name=keyword)
        except:
            city = City.objects.create(
                country=country,
                name=keyword
            )

        try:
            accommodationList = crawler.AccommodationList(keyword=keyword)
            for i in range(1):
                accommodationList.getAccommodationList(i)


            for accommodation in accommodationList.list:
                accommodation.getAccommodationDetail()
                time.sleep(2)

            for accommodation in accommodationList.list:
                try:
                    accommodation_model = Accommodation.objects.get(name=accommodation.name)
                except:

                    accommodation_model = Accommodation.objects.create(
                        name=accommodation.name,
                        description='호텔',
                        country=country,
                        city=city,
                        address=accommodation.location,
                        main_img_src=accommodation.hotel_img
                    )

                    for i in range(len(accommodation.thub_img_list)):
                        try:
                            Photo.objects.create(
                                thumb_img_src = accommodation.thub_img_list[i],
                                img_src = accommodation.img_list[i],
                                accommodation=accommodation_model
                            )
                        except:
                            pass
                        
                    for room in accommodation.room_list:
                        Room.objects.create(
                            name = room[0],
                            description = '방',
                            price = int(re.findall('\d+', room[1].replace(',',''))[0]),
                            guests = int(re.findall('\d+', room[2])[0]),
                            accommodation=accommodation_model
                        )

        except Exception as e:
            print(type(e))    
            print(e.args)     
            print(e) 

        self.stdout.write(self.style.SUCCESS("created!"))