from django.shortcuts import render

from rest_framework import viewsets, permissions
from .serializers import *
from .models import Uzytkownik


class UzytkownikView(viewsets.ModelViewSet):
    serializer_class = UzytkownikSerializer
    queryset = Uzytkownik.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        qs = super().get_queryset()
        current_status = str(self.request.query_params.get("status")).lower()

        if not bool(self.request.query_params):
            return qs

        return qs.filter(status=current_status)


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

    def get_queryset(self):
        qs = super().get_queryset()
        wydzial = str(self.request.query_params.get("wydzial")).lower()

        if not bool(self.request.query_params):
            return qs

        return qs.filter(id_wydzialu=wydzial)


class StudentView(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        qs = super().get_queryset()
        kierunek = str(self.request.query_params.get("kierunek")).lower()

        if not bool(self.request.query_params):
            return qs

        return qs.filter(id_kierunku=kierunek)


class RezerwacjaSaliView(viewsets.ModelViewSet):
    serializer_class = RezerwacjaSaliSerializer

    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        print(self.request.user)
        return self.request.user.uzytkownik.rezerwacje_sal.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class NewViewSet(viewsets.GenericViewSet):
    pass


class PracowniaSpecjalistycznaView(viewsets.ModelViewSet):
    serializer_class = PracowniaSpecjalistycznaSerializer
    queryset = PracowaniaSpecjalistyczna.objects.all()
    permission_classes = [
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
