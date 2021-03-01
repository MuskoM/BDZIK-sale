from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Wydzial(models.Model):
    id_wydzialu = models.AutoField(primary_key=True)
    nazwa_wydzialu = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.nazwa_wydzialu}'

    class Meta:
        verbose_name_plural = "Wydziały"


class Kierunek(models.Model):
    id_kierunku = models.AutoField(primary_key=True)
    nazwa_kierunku = models.CharField(max_length=30)
    id_wydzialu = models.ForeignKey(Wydzial, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nazwa_kierunku}'

    class Meta:
        verbose_name_plural = "Kierunki"


class Uzytkownik(models.Model):
    id_uzytkownika = models.AutoField(primary_key=True)
    konto = models.OneToOneField(User, on_delete=models.CASCADE)
    imie = models.CharField(max_length=15)
    nazwisko = models.CharField(max_length=25)
    e_mail = models.CharField(max_length=25)
    status = models.CharField(max_length=15)
    id_wydzialu = models.ForeignKey(Wydzial, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.imie == "" or self.nazwisko == "" or self.e_mail == "":
            raise ValidationError("Uzupełnij brakujące dane!")
        super(Uzytkownik, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.imie} {self.nazwisko}'

    class Meta:
        verbose_name_plural = "Użytkownicy"


class Student(models.Model):
    nr_indeksu = models.AutoField(primary_key=True)
    nr_telefonu = models.IntegerField()
    id_uzytkowanika = models.OneToOneField(Uzytkownik, on_delete=models.CASCADE)
    id_kierunku = models.ForeignKey(Kierunek, on_delete=models.CASCADE)

    # nie jestem pewien czy to jest dobrze bo krzyczy że ja chce inta a nr_telefonu to integerfield
    # niby nie jest na czerwono czyli chyba powinno to zadziałać ale nie mam pewności
    def save(self, *args, **kwargs):
        if 100000000 > self.nr_telefonu > 999999999:
            raise ValidationError("Nie ma takiego numeru telefonu! Podaj prawdziwy numer.")

    def __str__(self):
        return f'{self.nr_indeksu}'

    class Meta:
        verbose_name_plural = "Studenci"


class Pomieszczenie(models.Model):
    type_of_classroom = (
        ("S", "Sala"),
        ("L", "Laboratorium"),
        ("P", "Pracownia"),
        ("A", "Aula wykladowa")
    )

    id_pomieszczenia = models.AutoField(primary_key=True)
    id_wydzialu = models.ForeignKey(Wydzial, on_delete=models.CASCADE)
    opis = models.TextField()
    rodzaj_pom = models.CharField(max_length=1, choices=type_of_classroom, default="S")

    def __str__(self):
        return f' {self.id_pomieszczenia} : {self.rodzaj_pom} : {self.id_wydzialu}'

    class Meta:
        verbose_name_plural = "Pomieszczenia"


class RezerwacjaSali(models.Model):
    status_labels = (
        ("Z", "Zaakceptowana"),
        ("O", "Odrzucona"),
        ("R", "W trakcie rozpatrywania")
    )
    id_rezerwacji_sali = models.AutoField(primary_key=True)
    id_pomieszczenia = models.ForeignKey(Pomieszczenie, on_delete=models.CASCADE)
    data_od = models.DateTimeField()
    data_do = models.DateTimeField()
    id_uzytkownika = models.ForeignKey(Uzytkownik, related_name="rezerwacje_sal", on_delete=models.CASCADE)
    data_wykonania_rezerwacji = models.DateTimeField(default=datetime.now())
    status = models.CharField(max_length=1, choices=status_labels, default="R")

    def save(self, *args, **kwargs):
        if self.data_od < datetime.now() or self.data_do < datetime.now():
            raise ValidationError("Nie można użyć daty z przeszłości!")
        if self.data_od > self.data_do:
            raise ValidationError("Data początku rezerwacji poźniejsza od daty końca rezerwacji!")
        super(RezerwacjaSali, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.id_rezerwacji_sali}'

    class Meta:
        verbose_name_plural = "Rezerwacje Sal"


class PracowaniaSpecjalistyczna(Pomieszczenie):
    nr_pracowni = models.AutoField(primary_key=True)
    ilosc_miejsc = models.IntegerField()
    czy_rzutnik = models.BooleanField()
    osprzet = models.TextField()

    def __str__(self):
        return f'{self.nr_pracowni}'

    class Meta:
        verbose_name_plural = "Pracownie Specjalistyczne"


class Sala(Pomieszczenie):
    nr_sali = models.AutoField(primary_key=True)
    ilosc_miejsc = models.IntegerField()
    czy_rzutnik = models.BooleanField()
    jaka_tablica = models.TextField()

    def __str__(self):
        return f'Sala: {self.nr_sali}'

    class Meta:
        verbose_name_plural = "Sale"


class Laboratorium(Pomieszczenie):
    nr_laboratorium = models.AutoField(primary_key=True)
    ilosc_miejsc = models.IntegerField()
    czy_rzutnik = models.BooleanField()
    osprzet = models.TextField()

    def __str__(self):
        return f'Laboratorium {self.nr_laboratorium}'

    class Meta:
        verbose_name_plural = "Laboratoria"


class Akademik(models.Model):
    id_akademika = models.AutoField(primary_key=True)
    nazwa_akademika = models.CharField(max_length=25)

    def __str__(self):
        return f'{self.nazwa_akademika}'

    class Meta:
        verbose_name_plural = "Akademiki"


class Pokoj(models.Model):
    id_pokoju = models.AutoField(primary_key=True)
    id_akademika = models.ForeignKey(Akademik, on_delete=models.CASCADE)
    ilosc_lozek = models.IntegerField()
    opis = models.TextField()

    def __str__(self):
        return f'Pokoj {self.id_pokoju} Akademik {self.id_akademika}'

    class Meta:
        verbose_name_plural = "Pokoje"


class RezerwacjaPokoju(models.Model):
    status_labels = (
        ("Z", "Zaakceptowana"),
        ("O", "Odrzucona"),
        ("R", "W trakcie rozpatrywania")
    )
    id_rezerwacji_pokoju = models.AutoField(primary_key=True)
    id_pokoju = models.ForeignKey(Pokoj, on_delete=models.CASCADE)
    data_od = models.DateTimeField()
    data_do = models.DateTimeField()
    id_uzytkownika = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE)
    data_wykonania_rezerwacji = models.DateTimeField(default=datetime.now())
    status = models.CharField(max_length=1, choices=status_labels, default="R")

    def save(self, *args, **kwargs):
        if self.data_od < datetime.now() or self.data_do < datetime.now():
            raise ValidationError("Nie można użyć daty z przeszłości!")
        if self.data_od > self.data_do:
            raise ValidationError("Data początku rezerwacji poźniejsza od daty końca rezerwacji!")
        super(RezerwacjaPokoju, self).save(*args, **kwargs)

    def __str__(self):
        return f'Rezerwacja: {self.id_rezerwacji_pokoju} Użytkownik {self.id_uzytkownika}'

    class Meta:
        verbose_name_plural = "Rezerwacje Pokoi"
