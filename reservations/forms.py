from django import forms
from django.forms import ModelForm
from .models import Pomieszczenie

class ClassroomFilterForm(ModelForm):
    class Meta:
        model = Pomieszczenie
        fields = '__all__'
        widgets = {
            "rodzaj_pom": forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'exampleSelect1'
                }
            )
        }




