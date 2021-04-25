from django.db import models
from datetime import datetime
from django.utils import timezone
from django.db.models import Q,F
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def check_do_reservations_collide(begin_date,end_date,room_id):
    if begin_date > end_date:
        condition = (
                Q(data_od__gte=F('data_do')) |
                Q(data_od__lte=end_date) |
                Q(data_do__gte=begin_date)
        )
    else:
        condition = (
                Q(data_od__gte=F('data_do'), data_od__lte=end_date) |
                Q(data_od__gte=F('data_do'), data_do__gte=begin_date) |
                Q(data_od__lte=end_date, data_do__gte=begin_date)
        )

    colliding = RezerwacjaSali.objects.filter(id_pomieszczenia=room_id).filter(condition)

    if colliding:
        return True
    else:
        return False



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


    def save(self, *args, **kwargs):
        if 100000000 < self.nr_telefonu or self.nr_telefonu < 999999999:
            raise ValidationError("Nie ma takiego numeru telefonu! Podaj prawdziwy numer.")
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.nr_indeksu}'

    class Meta:
        verbose_name_plural = "Studenci"


class Pomieszczenie(models.Model):
    classroom_types = (
        ("S", "Sala"),
        ("L", "Laboratorium"),
        ("P", "Pracownia"),
        ("A", "Aula wykladowa")
    )

    id_pomieszczenia = models.AutoField(primary_key=True)
    id_wydzialu = models.ForeignKey(Wydzial, on_delete=models.CASCADE)
    opis = models.TextField()
    rodzaj_pom = models.CharField(max_length=1, choices=classroom_types, default="S")
    opiekun = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE, default=Uzytkownik.objects.first().pk)

    def __str__(self):
        return f'{self.get_rodzaj_pom_display()} {self.id_pomieszczenia}'

    class Meta:
        verbose_name_plural = "Pomieszczenia"


class Subject(models.Model):
    subject_type = (
        ("W", "Wykład"),
        ("C", "Ćwiczenia"),
        ("L", "Laboratorium"),
        ("P", "Pracownia Specjalistyczna"),
        ("S", "Seminarium")
    )

    subject_id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=50)
    subject_code = models.CharField(max_length=10)
    ECTS = models.IntegerField()
    subject_faculty = models.ForeignKey(Wydzial, on_delete=models.CASCADE)
    isObligatory = models.BooleanField(default=False)
    type = models.CharField(max_length=1, choices=subject_type, default="R")

    def __str__(self):
        return f'Przedmiot: {self.subject_name} Wydział {self.subject_faculty}'

    class Meta:
        verbose_name_plural = "Przedmioty"


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
    przedmiot = models.ForeignKey(Subject, on_delete=models.CASCADE,null=True)

    # def save(self, *args, **kwargs):
    #     if self.data_od < timezone.now() or self.data_do < timezone.now():
    #         raise ValidationError("Nie można użyć daty z przeszłości!")
    #     if self.data_od > self.data_do:
    #         raise ValidationError("Data początku rezerwacji poźniejsza od daty końca rezerwacji!")
    #     if check_do_reservations_collide(self.data_od,self.data_do,self.id_pomieszczenia):
    #         raise ValidationError("Rezerwacja koliduje z innymi")
    #     super(RezerwacjaSali, self).save(*args, **kwargs)

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



