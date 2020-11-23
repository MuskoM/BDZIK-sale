from django.contrib import admin
from .models import *


class Admin(admin.ModelAdmin):
    empty_value_display = '-puste-'


class UzytkownikAdmin(admin.ModelAdmin):
    fields = ['konto','imie', 'nazwisko', "e_mail", 'status','id_wydzialu']
    list_display = ('konto','id_uzytkownika', 'imie', 'nazwisko', "e_mail", 'status')


class WydzialAdmin(admin.ModelAdmin):
    list_display = ['nazwa_wydzialu']


class KierunekAdmin(admin.ModelAdmin):
    list_display = ['nazwa_kierunku', 'id_wydzialu']


class StudentAdmin(admin.ModelAdmin):
    list_display = ['id_uzytkowanika','nr_indeksu','nr_telefonu','id_kierunku']


class PomieszczenieAdmin(admin.ModelAdmin):
    list_display = ['id_pomieszczenia','id_wydzialu','opis','rodzaj_pom']


class RezerwacjaSaliAdmin(admin.ModelAdmin):
    list_display = ['id_rezerwacji_sali','id_pomieszczenia','data_od','data_do','id_uzytkownika']


class PracowaniaSpecjalistycznaAdmin(admin.ModelAdmin):
    list_display = ['nr_pracowni','ilosc_miejsc','czy_rzutnik','osprzet']


class SalaAdmin(admin.ModelAdmin):
    list_display = ['nr_sali','ilosc_miejsc','czy_rzutnik','jaka_tablica']


class LaboratoriumAdmin(admin.ModelAdmin):
    list_display = ['nr_laboratorium','ilosc_miejsc','czy_rzutnik','osprzet']


class AkademikAdmin(admin.ModelAdmin):
    list_display = ['nazwa_akademika']


class PokojAdmin(admin.ModelAdmin):
    list_display = ['id_pokoju','id_akademika','ilosc_lozek','opis']


class RezerwacjaPokojuAdmin(admin.ModelAdmin):
    list_display = ['id_pokoju','data_od','data_do','id_uzytkownika']


admin.site.register(Uzytkownik,UzytkownikAdmin)
admin.site.register(Wydzial,WydzialAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(Pomieszczenie,PomieszczenieAdmin)
admin.site.register(RezerwacjaSali,RezerwacjaSaliAdmin)
admin.site.register(PracowaniaSpecjalistyczna,PracowaniaSpecjalistycznaAdmin)
admin.site.register(Sala,SalaAdmin)
admin.site.register(Laboratorium,LaboratoriumAdmin)
admin.site.register(Akademik,AkademikAdmin)
admin.site.register(Pokoj,PokojAdmin)
admin.site.register(RezerwacjaPokoju,RezerwacjaPokojuAdmin)
admin.site.register(Kierunek,KierunekAdmin)