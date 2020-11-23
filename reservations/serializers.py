from rest_framework import serializers
from .models import *


class UzytkownikSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uzytkownik
        fields = ('id_uzytkownika','imie','nazwisko','e_mail','status','id_wydzialu')


class WydzialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wydzial
        fields = '__all__'


class KierunekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kierunek
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class RezerwacjaSaliSerializer(serializers.ModelSerializer):
    class Meta:
        model = RezerwacjaSali
        fields = '__all__'


class PracowniaSpecjalistycznaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PracowaniaSpecjalistyczna
        fields = '__all__'


class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = '__all__'


class LaboratoriumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laboratorium
        fields = '__all__'