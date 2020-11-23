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


class KierunekView(viewsets.ModelViewSet):
    serializer_class = KierunekSerializer
    queryset = Kierunek.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]


class StudentView(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]


class PomieszczenieView(viewsets.ModelViewSet):
    serializer_class = PomieszczenieSerializer
    queryset = Pomieszczenie.objects.all()
