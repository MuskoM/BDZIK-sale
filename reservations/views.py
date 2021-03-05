from django.shortcuts import render
from django.views import View
from .filters import PomieszczenieFilter,RezerwacjaSaliFilter

from reservations.models import Wydzial, Akademik, Pomieszczenie,RezerwacjaSali


class MainSite(View):



    def get(self, request):
        faculties = Wydzial.objects.all()
        dorms = Akademik.objects.all()

        context = {
            "faculties": faculties,
            "dormitories": dorms
        }

        return render(request, 'reservations/MainTemplate.html', context)


class FacultiesView(View):
    def get(self, request):

        classrooms_by_faculty = Pomieszczenie.objects.all()
        classrooms = PomieszczenieFilter(request.GET,queryset=classrooms_by_faculty)

        context = {
            "classrooms": classrooms,
        }
        return render(request, 'reservations/FacultiesTemplate.html', context)


class FacultyRoomView(View):
    room_types = {
        "S": "Sala wykładowa",
        "P": "Pracownia specjalistyczna",
        "L": "Laburatorium",
        "A": "Aula Wykładowa"
    }

    def get(self, request, room_id):

        room_id = room_id
        room = Pomieszczenie.objects.get(id_pomieszczenia=room_id)
        room_type = self.room_types[room.rodzaj_pom]

        context = {
            "classroom": room,
            "classroom_type": room_type
        }
        return render(request, "reservations/FacultyRoomTemplate.html", context)


class DormView(View):
    def get(self, request, dorm_id):
        return render(request, 'reservations/DormsTemplate.html')


class DormRoomView(View):
    def get(self, request, dorm_id, room_id):
        return render(request, "reservations/DormRoomTemplate.html")


class UserView(View):
    def get(self, request):
        return render(request, 'reservations/UserTemplate.html')


class UserEditView(View):
    def get(self, request):
        return render(request, 'reservations/UserEditTemplate.html')


class ReservationsView(View):
    def get(self, request):
        reservations = RezerwacjaSali.objects.all()
        reservations_filter = RezerwacjaSaliFilter(request.GET, queryset=reservations)

        context = {
            "reservations":reservations_filter
        }

        return render(request, 'reservations/ReservationsTemplate.html',
                      context)
