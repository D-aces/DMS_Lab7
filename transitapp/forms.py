from django import forms
from transitapp.models import Stops

class Stopform(forms.ModelForm):
    class Meta:
        model = Stops
        fields = ['stop_number', 'name']





