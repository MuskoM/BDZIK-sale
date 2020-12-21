from . import views
from django.urls import path, include

# router = routers.DefaultRouter()
# router.register('api/users', UzytkownikView, 'users')
# router.register('api/wydzialy',WydzialView,'wydzialy')
# router.register('api/kierunki',KierunekView,'kierunki')
# router.register('api/studenci',StudentView,'studenci')
# router.register('api/rezerwacje_sal',RezerwacjaSaliView,'rezerwacje_sal')
# router.register('api/pracownie_specjalistyczne',PracowniaSpecjalistycznaView,'pracownie_specjalistyczne')
# router.register('api/sale',SalaView,'sale')
# router.register('api/laboratoria',LaboratoriumView,'laboratoria')

urlpatterns = [

    path('', views.MainSite.as_view(), name='MainSite'),

]

urlpatterns += [

    path('accounts/', include('django.contrib.auth.urls')),

    path('faculty=<int:faculty_id>', views.FacultiesView.as_view(), name="FacultiesPage"),
    path('faculty=<int:faculty_id>/room=<int:room_id>', views.FacultyRoomView.as_view(), name="FacultyRoomPage"),

    path('dorm=<int:dorm_id>', views.DormView.as_view(), name="DormsPage"),
    path('dorm=<int:dorm_id>/room=<int:room_id>', views.DormRoomView, name="DormRoomPage"),

    path('user/', views.UserView.as_view(),name="UserPage"),
    path('user/detail', views.UserEditView.as_view(),name="UserEditPage"),
    path('user/reservations=<reservation_status>', views.UserReservationsView.as_view(),name="UserReservationsPage"),

]
