import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.mail import send_mail
from django.db.models import Q, F
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views import View
from .filters import PomieszczenieFilter, RezerwacjaSaliFilter
from .forms import NewClassroomReservationForm, ChangeClassroomReservationStatusForm, NewSubjectClassesReservationForm
from django.contrib.auth import get_user
from django.contrib import messages

from reservations.models import Wydzial, Akademik, Pomieszczenie, RezerwacjaSali, Uzytkownik, Subject


class MainSite(View):

    def get(self, request):
        faculties = Wydzial.objects.all()
        dorms = Akademik.objects.all()

        context = {
            "title": "PB",
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

        res = RezerwacjaSali.objects.first()
        all_reservations = RezerwacjaSali.objects.filter(id_pomieszczenia=room_id,status="Z")

        if request.GET:
            reservations_array = []
            for i in all_reservations:
                reserv_subarray = {}
                reserv_subarray['title'] = i.id_rezerwacji_sali
                start_date = datetime.datetime.strptime(str(i.data_od.date()), "%Y-%m-%d").strftime("%Y-%m-%d")
                end_date = datetime.datetime.strptime(str(i.data_do.date()), "%Y-%m-%d").strftime("%Y-%m-%d")
                reserv_subarray['start'] = start_date
                reserv_subarray['end'] = end_date
                reservations_array.append(reserv_subarray)

        context = {
            "classroom": room,
            "classroom_type": room_type,
            "events": all_reservations,
        }
        return render(request, "reservations/FacultyRoomTemplate.html", context)

    def post(self, request, room_id):
        new_reservation = NewClassroomReservationForm(request.POST)
        if new_reservation.is_valid():
            print(new_reservation)
            new_reservation_form = new_reservation.save(commit=False)
            new_reservation_form.id_pomieszczenia = Pomieszczenie.objects.get(pk=room_id)
            new_reservation_form.id_uzytkownika = request.user.uzytkownik
            new_reservation_form.opis=request.POST['comment']
            new_reservation_form.data_wykonania_rezerwacji = timezone.now()
            try:
                if check_do_reservations_collide(new_reservation_form.data_od,
                                                 new_reservation_form.data_do, new_reservation_form.id_pomieszczenia):
                    messages.error(request, "Rezerwacje kolidują z innymi")
                else:
                    new_reservation_form.save()
                    messages.success(request, "Pomyślnie wysłano prośbę o dokonanie rezerwacji.")
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
        today = timezone.now()

        context = {
            "today":today,
            "reservations": reservations
        }
        return render(request, 'reservations/ReservationsManagerTemplate.html', context)

    def post(self, request, reservation_id):
        print(reservation_id)
        new_status = ChangeClassroomReservationStatusForm(request.POST)
        reservation = RezerwacjaSali.objects.get(pk=reservation_id)
        print(reservation)

        print(request.POST)

        if request.POST['status'] == "Z":
            print("ZAAKCEPTOWANO")
            message_name = "Zaakceptowano rezerwację nr. " + str(reservation.id_rezerwacji_sali)
            message_email = reservation.id_uzytkownika.e_mail
            context = {
                'type': request.POST['status'],
                'user': reservation.id_uzytkownika,
                'reservation_date': reservation.data_wykonania_rezerwacji,
                'status': 'ZAAKCEPTOWANA'
            }
            html_message = render_to_string('mail_template.html', context)
            plain_message = strip_tags(html_message)

        elif request.POST['status'] == "O":
            print("ODRZUCONO")
            message_name = "Odrzucono rezerwację nr. " + str(reservation.id_rezerwacji_sali)
            message_email = reservation.id_uzytkownika.e_mail
            context = {
                'type': request.POST['status'],
                'user': reservation.id_uzytkownika,
                'reservation_date': reservation.data_wykonania_rezerwacji,
                'status': "ODRZUCONA",
                'comment': request.POST['comment'],
            }
            html_message = render_to_string('mail_template.html', context)
            plain_message = strip_tags(html_message)

        else:
            print("KOMENTARZ")
            message_name = "Nowy komentarz do rezerwacji nr. " + str(reservation.id_rezerwacji_sali)
            message_email = reservation.id_uzytkownika.e_mail
            context = {
                'type': request.POST['status'],
                'user': reservation.id_uzytkownika,
                'reservation_date': reservation.data_wykonania_rezerwacji,
                'comment': request.POST['comment'],
            }
            html_message = render_to_string('mail_template.html', context)
            plain_message = strip_tags(html_message)

            send_mail(message_name,
                      plain_message,
                      'admin-e53753@inbox.mailtrap.io',
                      [message_email],
                      html_message=html_message)

        if new_status.is_valid():
            reservation.status = new_status.cleaned_data['status']
            print("Reservation_status: ", reservation)
            send_mail(message_name,
                      plain_message,
                      'admin-e53753@inbox.mailtrap.io',
                      [message_email],
                      html_message=html_message)
            print("Sent Mail")
            reservation.save()

        return redirect(request.META.get('HTTP_REFERER'))


class ClassManager(View):

    def get(self, request):
        check_classroom_reservations = RezerwacjaSali.objects.all()
        subjects_all = Subject.objects.filter(subject_faculty=request.user.uzytkownik.id_wydzialu)
        classrooms_all = Pomieszczenie.objects.all()
        context = {
            "subjects_all": subjects_all,
            "reservations_all": check_classroom_reservations,
            "classrooms_all": classrooms_all
        }
        return render(request, 'reservations/ClassManagerTemplate.html', context)

    def post(self, request):
        new_class_res_form = NewSubjectClassesReservationForm(request.POST)

        if new_class_res_form.is_valid():
            new_reservation_form = new_class_res_form.save(commit=False)
            new_reservation_form.id_uzytkownika = request.user.uzytkownik
            new_reservation_form.data_wykonania_rezerwacji = timezone.now()
            new_reservation_form.status = 'Z'
            new_reservation_form.save()

        context = {
            'request': request.POST
        }

        return redirect('ClassManager')


class UserEditView(View):
    def get(self, request):
        return render(request, 'reservations/UserPermissionsPanelTemplate.html')


class UserPermissionsPanelView(View):
    def get(self, request):
        return render(request, 'reservations/UserPermissionsPanelTemplate.html')

    def post(self, request):
        return render(request, 'reservations/UserPermissionsPanelTemplate.html')


class ReservationsView(View):
    def get(self, request):
        reservations = RezerwacjaSali.objects.filter(status="Z")
        reservations_filter = RezerwacjaSaliFilter(request.GET, queryset=reservations)

        context = {
            "reservations": reservations_filter
        }

        return render(request, 'reservations/ReservationsTemplate.html',
                      context)
