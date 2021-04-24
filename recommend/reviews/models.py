from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import TimeStampedModel

# Create your models here.
class Review(TimeStampedModel):
    """ Review Model Definition """
    review = models.TextField()
    cleanliness = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    kindness = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    location = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    comfortable = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    facility = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    cost = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    accommodation = models.ForeignKey(
        "accommodations.Accommodation", related_name="reviews", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.review} - {self.accommodation}"

    def rating_average(self):
        avg = (
            self.cleanliness
            + self.kindness
            + self.location
            + self.comfortable
            + self.facility
            + self.cost
        ) / 6
        return round(avg, 2)

    rating_average.short_description = "Avg."

    class Meta:
        ordering = ("-created",)