from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.mail import send_mail
from django.db.models import Q, F
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views import View
from .filters import PomieszczenieFilter, RezerwacjaSaliFilter
from .forms import NewClassroomReservationForm, ChangeClassroomReservationStatusForm
from django.contrib.auth import get_user
from django.contrib import messages

from reservations.models import Wydzial, Akademik, Pomieszczenie, RezerwacjaSali, Uzytkownik


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
        classrooms = PomieszczenieFilter(request.GET, queryset=classrooms_by_faculty)

        context = {
            "classrooms": classrooms,
        }
        return render(request, 'reservations/FacultiesTemplate.html', context)


def check_do_reservations_collide(begin_date, end_date, room_id):
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

    def post(self, request, room_id):
        new_reservation = NewClassroomReservationForm(request.POST)
        if new_reservation.is_valid():
            new_reservation_form = new_reservation.save(commit=False)
            new_reservation_form.id_pomieszczenia = Pomieszczenie.objects.get(pk=room_id)
            new_reservation_form.id_uzytkownika = request.user.uzytkownik
            new_reservation_form.data_od = new_reservation.cleaned_data['data_od']
            new_reservation_form.data_do = new_reservation.cleaned_data['data_do']
            try:
                if check_do_reservations_collide(new_reservation_form.data_od,
                                                 new_reservation_form.data_do, new_reservation_form.id_pomieszczenia):
                    messages.error(request, "Rezerwacje kolidują z innymi")
                else:
                    new_reservation_form.save()
                    messages.success(request, "Pomyślnie dokonano rezerwacji")
            except ValidationError:
                messages.error(request, "Błąd w dokonywaniu rezerwacji")
        return redirect('FacultyRoomPage', room_id)


class DormView(View):
    def get(self, request, dorm_id):
        return render(request, 'reservations/DormsTemplate.html')


class DormRoomView(View):
    def get(self, request, dorm_id, room_id):
        return render(request, "reservations/DormRoomTemplate.html")


class UserView(View):
    def get(self, request):
        current_user = get_user(request)

        try:
            user = Uzytkownik.objects.get(pk=current_user.pk)
        except ObjectDoesNotExist:
            return redirect('login')

        made_reservations = RezerwacjaSali.objects.order_by('-data_od').filter(id_uzytkownika=current_user.pk)
        context = {
            "username": user,
            "made_reservations": made_reservations
        }

        return render(request, 'reservations/UserTemplate.html', context)


class ReservationManagerView(View):
    def get(self, request):
        reservations = RezerwacjaSali.objects.all()

        context = {
            "reservations": reservations
        }
        return render(request, 'reservations/ReservationsManagerTemplate.html', context)

    def post(self, request, reservation_id):
        new_status = ChangeClassroomReservationStatusForm(request.POST)
        reservation = RezerwacjaSali.objects.get(pk=reservation_id)
        print()
        if request.POST['status'] == "Z":
            message_name = "Zaakceptowano rezerwację nr. " + str(reservation.id_rezerwacji_sali)
            message_email = reservation.id_uzytkownika.e_mail
            context = {
                'user': reservation.id_uzytkownika,
                'reservation_date': str(reservation.data_wykonania_rezerwacji),
                'status': 'ZAAKCEPTOWANA'
            }
            html_message = render_to_string('mail_template.html', context)
            plain_message = strip_tags(html_message)
        else:
            message_name = "Odrzucono rezerwację nr. " + str(reservation.id_rezerwacji_sali)
            message_email = reservation.id_uzytkownika.e_mail
            context = {
                'user': reservation.id_uzytkownika,
                'reservation_date': str(reservation.data_wykonania_rezerwacji),
                'status': "ODRZUCONA"
            }
            html_message = render_to_string('mail_template.html', context)
            plain_message = strip_tags(html_message)

        if new_status.is_valid():
            reservation.status = new_status.cleaned_data['status']
            send_mail(message_name,
                      plain_message,
                      'admin-e53753@inbox.mailtrap.io',
                      [message_email],
                      html_message=html_message)
            reservation.save()

        return redirect(request.META.get('HTTP_REFERER'))


class UserEditView(View):
    def get(self, request):
        return render(request, 'reservations/UserPermissionsPanelTemplate.html')


class UserPermissionsPanelView(View):
    def get(self,request):

        return render(request, 'reservations/UserPermissionsPanelTemplate.html')

    def post(self,request):

        return render(request, 'reservations/UserPermissionsPanelTemplate.html')


class ReservationsView(View):
    def get(self, request):
        reservations = RezerwacjaSali.objects.all()
        reservations_filter = RezerwacjaSaliFilter(request.GET, queryset=reservations)

        context = {
            "reservations": reservations_filter
        }

        return render(request, 'reservations/ReservationsTemplate.html',
                      context)