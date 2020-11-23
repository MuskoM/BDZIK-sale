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
    permission_classes = [
        permissions.AllowAny
    ]


class RezerwacjaSaliView(viewsets.ModelViewSet):
    serializer_class = RezerwacjaSaliSerializer

    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        return self.request.user.uzytkownik.rezerwacje_sal.all()


class PracowniaSpecjalistycznaView(viewsets.ModelViewSet):
    serializer_class = PracowniaSpecjalistycznaSerializer
    queryset = PracowaniaSpecjalistyczna.objects.all()
    permission_classes =  [
        permissions.AllowAny
    ]


class SalaView(viewsets.ModelViewSet):
    serializer_class = SalaSerializer
    queryset = Sala.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]


class LaboratoriumView(viewsets.ModelViewSet):
    serializer_class = LaboratoriumSerializer
    queryset = Laboratorium.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]