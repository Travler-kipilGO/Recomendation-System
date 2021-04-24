import datetime
from django.db import models
from django.utils import timezone
from core.models import TimeStampedModel
# Create your models here.

class BookedDay(TimeStampedModel):
    day = models.DateField()
    reservation = models.ForeignKey('Reservation', on_delete=models.CASCADE)
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Booked Day"
        verbose_name_plural = "Booked Days"

    def __str__(self):
        return str(self.day)


class Reservation(TimeStampedModel):
    """ 예약 """
    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceled"),
    )

    accommodation = models.ForeignKey(
        'accommodations.Accommodation', related_name="reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        'rooms.Room', related_name="reservations", on_delete=models.CASCADE
    )
    guest = models.ForeignKey(
        "users.User", related_name="reservations", on_delete=models.CASCADE
    )
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    email = models.EmailField()
    cost = models.IntegerField()
    paid = models.BooleanField(default=False)

   
    def save(self, *args, **kwargs):
        if self.pk is None:
            start = self.check_in
            end = self.check_out
            difference = end - start
            existing_booked_day = BookedDay.objects.filter(
                day__range=(start, end)
            ).exists()
            if not existing_booked_day:
                super().save(*args, **kwargs)
                for i in range(difference.days + 1):
                    day = start + datetime.timedelta(days=i)
                    BookedDay.objects.create(day=day, reservation=self)
                return
        return super().save(*args, **kwargs)

class Payment(TimeStampedModel):
    pass