from . import views
from django.urls import path, include


urlpatterns = [

    path('', views.MainSite.as_view(), name='MainSite'),

]

urlpatterns += [

    path('accounts/', include('django.contrib.auth.urls')),
    path('faculty/', views.FacultiesView.as_view(), name="FacultiesPage"),
    path('faculty/room=<int:room_id>', views.FacultyRoomView.as_view(), name="FacultyRoomPage"),

    path('reservations/',views.ReservationsView.as_view(), name="ReservationsView"),


    path('dorm=<int:dorm_id>', views.DormView.as_view(), name="DormsPage"),
    path('dorm=<int:dorm_id>/room=<int:room_id>', views.DormRoomView, name="DormRoomPage"),

    path('user/', views.UserView.as_view(),name="UserPage"),
    path('user/detail', views.UserEditView.as_view(),name="UserEditPage"),

]
