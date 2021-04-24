from django.views.generic import ListView, DetailView
from . import models

class AccommodationView(ListView):
    """ AccommodationView Definition """
    model = models.Accommodation
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "accommodations"


class AccommodationDetail(DetailView):
    """ AccommodationDetail Definition """
    model = models.Accommodation
    context_object_name = "accommodation"

