import datetime
from django.shortcuts import render, redirect, reverse
from accommodations.models import Accommodation
from . import models
# Create your views here.

def create(request, accommodation):
    try:
        date_obj = datetime.datetime.today()
        accommodation = Accommodation.objects.get(pk=accommodation)
        models.BookedDay.objects.get(day=date_obj, reservation__accommodation=accommodation)

    except models.BookedDay.DoesNotExist:
        reservation = models.Reservation.objects.create(
            guest=request.user,
            accommodation=accommodation,
            check_in=date_obj,
            check_out=date_obj + datetime.timedelta(days=1),
        )
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))