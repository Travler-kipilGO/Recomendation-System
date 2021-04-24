from django import forms
from . import models

class CreateReviewForm(forms.ModelForm):
    cleanliness = forms.IntegerField(max_value=10, min_value=0)
    kindness = forms.IntegerField(max_value=10, min_value=0)
    location = forms.IntegerField(max_value=10, min_value=0)
    comfortable = forms.IntegerField(max_value=10, min_value=0)
    facility = forms.IntegerField(max_value=10, min_value=0)
    cost = forms.IntegerField(max_value=10, min_value=0)
  
    class Meta:
        model = models.Review
        fields = (
            "review",
            "cleanliness",
            "kindness",
            "location",
            "comfortable",
            "facility",
            "cost",
        )

    def save(self):
        review = super().save(commit=False)
        return review