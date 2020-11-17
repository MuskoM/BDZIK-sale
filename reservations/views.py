from django.shortcuts import render

from rest_framework import  viewsets
from .serializers import UzytkownikSerializer
from .models import Uzytkownik


class UzytkownikView(viewsets.ModelViewSet):
    serializer_class = UzytkownikSerializer
    queryset = Uzytkownik.objects.all()

