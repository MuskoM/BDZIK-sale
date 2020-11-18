from django.shortcuts import render

from rest_framework import viewsets,permissions
from .serializers import *
from .models import Uzytkownik


class UzytkownikView(viewsets.ModelViewSet):
    serializer_class = UzytkownikSerializer
    queryset = Uzytkownik.objects.all()


class WydzialView(viewsets.ModelViewSet):
    serializer_class = WydzialSerializer
    queryset = Wydzial.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]