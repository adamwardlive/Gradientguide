from django import forms
from .models import TrainingSession

class TrainingSessionForm(forms.ModelForm):
    class Meta:
        model = TrainingSession
        fields = ['duration', 'power', 'weight',]
        
starting_location = forms.CharField(required=True)