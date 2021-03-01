import django_filters
from .models import Pomieszczenie,RezerwacjaSali,Uzytkownik


class PomieszczenieFilter(django_filters.FilterSet):
    opis = django_filters.CharFilter(lookup_expr='contains')

    class Meta:
        model = Pomieszczenie
        fields = '__all__'


class RezerwacjaSaliFilter(django_filters.FilterSet):
    data_od = django_filters.DateFilter(lookup_expr='contains', label="Data od")
    data_do = django_filters.DateFilter(lookup_expr='contains',label="Data do")
    id_uzytkownika = django_filters.ModelChoiceFilter(queryset=Uzytkownik.objects.all(), label="Użytkownik")
    id_pomieszczenia = django_filters.ModelChoiceFilter(queryset=Pomieszczenie.objects.all(), label="Pomieszczenie")

    class Meta:
        model = RezerwacjaSali
        fields = '__all__'
        exclude = ['data_wykonania_rezerwacji']
