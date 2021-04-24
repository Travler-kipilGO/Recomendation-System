import random
from django.core.management.base import BaseCommand
from reviews import models as review_models
from users import models as user_models
from accommodations import models as accommodation_models


class Command(BaseCommand):

    help = "This command creates reviews"

    def handle(self, *args, **options):
        users = user_models.User.objects.all()
        accommodations = accommodation_models.Accommodation.objects.all()
        accommodation_count = int(accommodation_models.Accommodation.objects.count() / 5)
        

        for user in users[:]:
            for i in range(accommodation_count):
                review_models.Review.objects.create(
                    review='test review',
                    cleanliness= random.randint(0, 6),
                    kindness= random.randint(0, 6),
                    location= random.randint(0, 6),
                    comfortable= random.randint(0, 6),
                    facility= random.randint(0, 6),
                    cost= random.randint(0, 6),
                    accommodation= random.choice(accommodations),
                    user=user,
                )
 

        self.stdout.write(self.style.SUCCESS("reviews created!"))