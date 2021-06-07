import datetime

from django.contrib import messages
from django.contrib.auth import get_user
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.mail import send_mail
from django.db.models import Q, F
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from django.views import View

from reservations.models import Wydzial, Akademik, Pomieszczenie, RezerwacjaSali, Uzytkownik, Subject, Pokoj, RezerwacjaPokoju
from .filters import PomieszczenieFilter, RezerwacjaSaliFilter, PokojFilter, DormRezerwacjeManageFilter
from .filters import RezerwacjeManageFilter
from .forms import NewClassroomReservationForm, ChangeClassroomReservationStatusForm, NewSubjectClassesReservationForm, \
    DeleteSubjectClassesReservationForm, NewDormRoomReservationForm, ChangeDormRoomReservationStatusForm


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


class FacultiesView(LoginRequiredMixin, View):
    login_url = "/registration/login"
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


class FacultyRoomView(LoginRequiredMixin, View):
    login_url = "/registration/login"
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


class DormView(LoginRequiredMixin, View):
    login_url = "/registration/login"
    def get(self, request):
        dorm_room = Pokoj.objects.all()
        dormrooms = PokojFilter(request.GET, queryset=dorm_room)
        context = {
            "dormrooms": dormrooms,
        }
        return render(request, 'reservations/DormsTemplate.html', context)


class DormRoomView(LoginRequiredMixin, View):
    login_url = "/registration/login"

    def get(self, request, room_id):
        room = Pokoj.objects.get(id_pokoju=room_id)

        context = {
            "room": room
        }
        return render(request, "reservations/DormRoomTemplate.html",context)


class UserView(View):
    def get(self, request):
        current_user = request.user
        groups = current_user.groups.all()
        is_coordinator = groups.filter(name="Koordynator").exists()
        is_admin = groups.filter(name__icontains="Administrator").exists()
        is_room_administrator = groups.filter(name="Opiekun").exists()
        is_dorm_admin = groups.filter(name__icontains="akademików").exists()

        print(is_coordinator,is_admin,is_room_administrator,is_dorm_admin)

        try:
            user = Uzytkownik.objects.get(pk=current_user.pk)
        except ObjectDoesNotExist:
            return redirect('login')

        made_reservations = RezerwacjaSali.objects.order_by('-data_od').filter(id_uzytkownika=current_user.pk)
        context = {
            "username": user,
            "is_coordinator": is_coordinator,
            "is_admin": is_admin,
            "is_room_administrator":is_room_administrator,
            "is_dorm_admin": is_dorm_admin,
            "made_reservations": made_reservations
        }

        return render(request, 'reservations/UserTemplate.html', context)


class ReservationManagerView(View):
    def get(self, request):
        current_user = get_user(request)
        reservations = RezerwacjaSali.objects.filter(id_pomieszczenia__opiekun=current_user.pk)
        reservations_filter = RezerwacjeManageFilter(request.GET, queryset=reservations)
        today = timezone.now()

        context = {
            "today": today,
            "reservations": reservations_filter
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
            }
            html_message = render_to_string('mail_template.html', context)
            plain_message = strip_tags(html_message)

        else:
            message_name = "ERROR." + str(reservation.id_rezerwacji_sali)
            message_email = reservation.id_uzytkownika.e_mail
            html_message = render_to_string('mail_template.html')
            plain_message = strip_tags(html_message)

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
        print(request.POST)
        new_class_res_form = NewSubjectClassesReservationForm(request.POST)
        delete_class_res_form = DeleteSubjectClassesReservationForm(request.POST)
        if delete_class_res_form.is_valid():
            found_res = RezerwacjaSali.objects.filter(id_rezerwacji_sali=request.POST['id_rezerwacji_sali'])
            found_res.delete()
        elif new_class_res_form.is_valid():
            new_reservation_form = new_class_res_form.save(commit=False)
            new_reservation_form.id_uzytkownika = request.user.uzytkownik
            new_reservation_form.data_wykonania_rezerwacji = timezone.now()
            new_reservation_form.status = 'Z'
            if new_reservation_form.cykliczny:
                for i in range(0, new_reservation_form.how_many_times):
                    periodic_res_form = new_reservation_form
                    periodic_res_form.pk = None
                    if i != 0:
                        periodic_res_form.data_od = periodic_res_form.data_od + timezone.timedelta(days=7)
                        periodic_res_form.data_do = periodic_res_form.data_do + timezone.timedelta(days=7)
                    periodic_res_form.save()
            else:
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
        users = Uzytkownik.objects.all()
        groups = Group.objects.all()

        context = {
            "users": users,
            "groups": groups
        }

        return render(request, 'reservations/UserPermissionsPanelTemplate.html',context)

    def post(self, request):
        print(request.POST)
        if "group-name" in request.POST:
            group_to_delete = Group.objects.get(name=request.POST['group-name'])
            user = Uzytkownik.objects.get(pk=request.POST['user-id'])
            group_to_delete.user_set.remove(user.konto)

        if "groups" in request.POST:
            groups = request.POST.getlist("groups")
            print(len(groups))
            for group in groups:
                group_to_add = Group.objects.get(name=group)
                user = Uzytkownik.objects.get(pk=request.POST['user-id'])
                group_to_add.user_set.add(user.konto)

        return redirect('PermissionsManager')


class ReservationsView(View):
    def get(self, request):
        reservations = RezerwacjaSali.objects.filter(status="Z")
        reservations_filter = RezerwacjaSaliFilter(request.GET, queryset=reservations)

        context = {
            "reservations": reservations_filter
        }

        return render(request, 'reservations/ReservationsTemplate.html',
                      context)


class DormReservationManagerView(View):
    def get(self, request):
        current_user = get_user(request)
        # reservations = RezerwacjaPokoju.objects.filter(id_pokoju__opiekun=current_user.pk)
        reservations = RezerwacjaPokoju.objects
        reservations_filter = DormRezerwacjeManageFilter(request.GET, queryset=reservations)
        today = timezone.now()

        context = {
            "today": today,
            "reservations": reservations_filter
        }
        return render(request, 'reservations/DormReservationsManagerTemplate.html', context)

    def post(self, request, reservation_id):
        print(reservation_id)
        new_status = ChangeDormRoomReservationStatusForm(request.POST)
        reservation = RezerwacjaPokoju.objects.get(pk=reservation_id)
        print(reservation)

        print(request.POST)

        if request.POST['status'] == "Z":
            print("ZAAKCEPTOWANO")
            message_name = "Zaakceptowano rezerwację nr. " + str(reservation.id_rezerwacji_pokoju)
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
            message_name = "Odrzucono rezerwację nr. " + str(reservation.id_rezerwacji_pokoju)
            message_email = reservation.id_uzytkownika.e_mail
            context = {
                'type': request.POST['status'],
                'user': reservation.id_uzytkownika,
                'reservation_date': reservation.data_wykonania_rezerwacji,
                'status': "ODRZUCONA",
            }
            html_message = render_to_string('mail_template.html', context)
            plain_message = strip_tags(html_message)

        else:
            message_name = "ERROR." + str(reservation.id_rezerwacji_pokoju)
            message_email = reservation.id_uzytkownika.e_mail
            html_message = render_to_string('mail_template.html')
            plain_message = strip_tags(html_message)

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
