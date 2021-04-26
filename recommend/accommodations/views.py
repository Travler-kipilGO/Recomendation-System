from django.views.generic import ListView, DetailView
from accommodations.models import Accommodation
import core.recommend as recommend
from users.models import User
from . import models

class AccommodationView(ListView):
    """ AccommodationView Definition """
    model = models.Accommodation
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "accommodations"

    def get_context_data(self, **kwargs):
        context = super(AccommodationView, self).get_context_data(**kwargs)
        recommends = recommend.get_k_neighbors(self.request.user.username, 3)
        context['recommends'] = (
            Accommodation.objects.get(name=recommends[0]),
            Accommodation.objects.get(name=recommends[1]),
            Accommodation.objects.get(name=recommends[2])
        )
        return context


class AccommodationDetail(DetailView):
    """ AccommodationDetail Definition """
    model = models.Accommodation
    context_object_name = "accommodation"

