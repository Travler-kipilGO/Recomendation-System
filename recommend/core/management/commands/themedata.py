import random
from django.core.management.base import BaseCommand
from reviews import models as review_models
from users import models as user_models
from accommodations import models as accommodation_models


class Command(BaseCommand):

    help = "This command creates reviews"

    def handle(self, *args, **options):
        users = user_models.User.objects.all()

        for user in users[:]:
            
            samplelist = random.sample(['A0101', 'A0201', 'A0202', 'A0203', 'A0206', 'A0207', 'A0208', 'A0302', 'A0401', 'A0502', 'B0201'], 5)

            user_models.Survey.objects.create(
                user=user,
                theme=samplelist[0],
            )
            user_models.Survey.objects.create(
                user=user,
                theme=samplelist[1],
            )
            user_models.Survey.objects.create(
                user=user,
                theme=samplelist[2],
            )
            user_models.Survey.objects.create(
                user=user,
                theme=samplelist[3],
            )
            user_models.Survey.objects.create(
                user=user,
                theme=samplelist[4],
            )

        self.stdout.write(self.style.SUCCESS("reviews created!"))