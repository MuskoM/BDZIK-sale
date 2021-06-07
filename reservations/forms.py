from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import RezerwacjaSali,Pomieszczenie


class NewClassroomReservationForm(forms.ModelForm):

    class Meta:
        model = RezerwacjaSali
        fields = ['data_od','data_do']

    def clean(self):
        super(NewClassroomReservationForm, self).clean()
        print(self.cleaned_data)
        data_od = self.cleaned_data.get('data_od')
        data_do = self.cleaned_data.get('data_do')
        if data_od < timezone.now() or data_do < timezone.now():
            raise ValidationError("Nie można użyć daty z przeszłości!")
        if data_od > data_do:
            raise ValidationError("Data początku rezerwacji poźniejsza od daty końca rezerwacji!")



class ChangeClassroomReservationStatusForm(forms.ModelForm):

    class Meta:
        model = RezerwacjaSali
        fields = ["status"]


class NewSubjectClassesReservationForm(forms.ModelForm):

    class Meta:
        model = RezerwacjaSali
        fields = ['data_od', 'data_do', 'id_pomieszczenia', 'przedmiot', 'cykliczny', 'how_many_times']


class DeleteSubjectClassesReservationForm(forms.ModelForm):

    class Meta:
        model = RezerwacjaSali
        fields = ['id_rezerwacji_sali']


class NewClassroomForm(forms.ModelForm):
    class Meta:
        model = Pomieszczenie
        fields = '__all__'
