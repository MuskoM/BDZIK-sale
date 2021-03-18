from . import views
from django.urls import path, include, re_path
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [

    path('', views.MainSite.as_view(), name='MainSite'),

]

urlpatterns += [

    path('registration/', include('django.contrib.auth.urls')),
    path('classrooms/', views.FacultiesView.as_view(), name="FacultiesPage"),
    path('classrooms/room=<int:room_id>', views.FacultyRoomView.as_view(), name="FacultyRoomPage"),


    path('reservations/',views.ReservationsView.as_view(), name="ReservationsView"),


    path('dorm=<int:dorm_id>', views.DormView.as_view(), name="DormsPage"),
    path('dorm=<int:dorm_id>/room=<int:room_id>', views.DormRoomView, name="DormRoomPage"),

    path('user/', views.UserView.as_view(),name="UserPage"),
    path('user/detail', views.UserEditView.as_view(),name="UserEditPage"),

]
