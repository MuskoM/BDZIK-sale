from rest_framework import serializers
from .models import Uzytkownik


class UzytkownikSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uzytkownik
        fields = ('id_uzytkownika','imie','nazwisko','e_mail','status','id_wydzialu')