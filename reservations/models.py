from django.db import models
from datetime import datetime


class Wydzial(models.Model):
    id_wydzialu = models.AutoField(primary_key=True)
    nazwa_wydzialu = models.CharField(max_length=30)


class Kierunek(models.Model):
    id_kierunku = models.AutoField(primary_key=True)
    nazwa_kierunku = models.CharField(max_length=30)
    id_wydzialu = models.ForeignKey(Wydzial, on_delete=models.CASCADE)


class Uzytkownik(models.Model):
    id_uzytkownika = models.AutoField(primary_key=True)
    imie = models.CharField(max_length=15)
    nazwisko = models.CharField(max_length=25)
    e_mail = models.CharField(max_length=25)
    status = models.CharField(max_length=15)
    id_wydzialu = models.ForeignKey(Wydzial, on_delete=models.CASCADE)


class Student(models.Model):
    nr_indeksu = models.AutoField(primary_key=True)
    nr_telefonu = models.IntegerField()
    id_uzytkowanika = models.OneToOneField(Uzytkownik, on_delete=models.CASCADE)
    id_kierunku = models.ForeignKey(Kierunek, on_delete=models.CASCADE)


class Pomieszczenie(models.Model):
    id_pomieszczenia = models.AutoField(primary_key=True)
    id_wydzialu = models.ForeignKey(Wydzial, on_delete=models.CASCADE)
    opis = models.TextField()
    rodzaj_pom = models.CharField(max_length=30)


class RezerwacjaSali(models.Model):
    id_rezerwacji_sali = models.AutoField(primary_key=True)
    id_pomieszczenia = models.ForeignKey(Pomieszczenie, on_delete=models.CASCADE)
    data_od = models.DateTimeField()
    data_do = models.DateTimeField()
    id_uzytkownika = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE)
    data_wykonania_rezerwacji = models.DateTimeField(default=datetime.now())


class PracowaniaSpecjalistyczna(Pomieszczenie):
    nr_pracowni = models.AutoField(primary_key=True)
    ilosc_miejsc = models.IntegerField()
    czy_rzutnik = models.BooleanField()
    osprzet = models.TextField()


class Sala(Pomieszczenie):
    nr_sali = models.AutoField(primary_key=True)
    ilosc_miejsc = models.IntegerField()
    czy_rzutnik = models.BooleanField()
    jaka_tablica = models.TextField()


class Laboratorium(Pomieszczenie):
    nr_laboratorium = models.AutoField(primary_key=True)
    ilosc_miejsc = models.IntegerField()
    czy_rzutnik = models.BooleanField()
    osprzet = models.TextField()


class Akademik(models.Model):
    id_akademika = models.AutoField(primary_key=True)
    nazwa_akademika = models.CharField(max_length=25)


class Pokoj(models.Model):
    id_pokoju = models.AutoField(primary_key=True)
    id_akademika = models.ForeignKey(Akademik,on_delete=models.CASCADE)
    ilosc_lozek = models.IntegerField()
    opis = models.TextField()


class RezerwacjaPokoju(models.Model):
    id_rezerwacji_pokoju = models.AutoField(primary_key=True)
    id_pokoju = models.ForeignKey(Pokoj,on_delete=models.CASCADE)
    data_od = models.DateTimeField()
    data_do = models.DateTimeField()
    id_uzytkownika = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE)
    data_wykonania_rezerwacji = models.DateTimeField(default=datetime.now())
