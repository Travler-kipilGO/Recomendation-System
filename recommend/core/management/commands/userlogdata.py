import random
import datetime
from django.core.management.base import BaseCommand
from travels import models as travel_models
from users import models as user_models


class Command(BaseCommand):

    help = "This command creates reviews"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many users you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")

        users = user_models.User.objects.all()
        travelspots = travel_models.TravelSpot.objects.all()

        for user in users[:]:
            for i in range(number):
                travel_models.UserLogData.objects.create(
                    user = user,
                    travelspot = random.choice(travelspots),
                    click = random.randint(1, 5),
                    date = datetime.date(random.randint(2019,2021), random.randint(1,12), random.randint(1,28))
                )
 

        self.stdout.write(self.style.SUCCESS("log created!"))