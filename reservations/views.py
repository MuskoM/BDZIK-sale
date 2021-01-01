from django.shortcuts import render
from django.views import View

from reservations.models import Wydzial, Akademik, Pomieszczenie


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
    def get(self, request, faculty_id):
        faculty_id = faculty_id
        faculty = Wydzial.objects.get(id_wydzialu=faculty_id)
        classrooms = Pomieszczenie.objects.filter(id_wydzialu=faculty_id)

        context = {
            "faculty_name": faculty,
            "faculty_id": faculty_id,
            "classrooms": classrooms
        }
        return render(request, 'reservations/FacultiesTemplate.html', context)


class FacultyRoomView(View):
    def get(self, request, faculty_id, room_id):
        return render(request, "reservations/FacultyRoomTemplate.html")


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


class UserReservationsView(View):
    def get(self, request, reservation_status):
        return render(request, 'reservations/UserReservationsTemplate.html',
                      context={"status": reservation_status})
