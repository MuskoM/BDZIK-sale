import django_filters
from .models import Pomieszczenie

class PomieszczenieFilter(django_filters.FilterSet):
    opis = django_filters.CharFilter(lookup_expr='contains')

    class Meta:
        model = Pomieszczenie
        fields = '__all__'
