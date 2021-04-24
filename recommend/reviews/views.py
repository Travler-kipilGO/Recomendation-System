from django.shortcuts import redirect, reverse
from accommodations.models import Accommodation
from . import forms


def create_review(request, accommodation_key):
    if request.method == "POST":
        form = forms.CreateReviewForm(request.POST)
        accommodation = Accommodation.objects.get_or_none(pk=accommodation_key)
        if not accommodation:
            return redirect(reverse("core:home"))
        if form.is_valid():
            review = form.save()
            review.accommodation = accommodation
            review.user = request.user
            review.save()
            return redirect(reverse("accommodations:detail", kwargs={"pk": accommodation.pk}))