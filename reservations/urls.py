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



    path('reservations/', views.ReservationsView.as_view(), name="ReservationsView"),


    path('dorms/', views.DormView.as_view(), name="DormsPage"),
    path('dorms/room=<int:room_id>', views.DormRoomView.as_view(), name="DormRoomPage"),

    path('user/', views.UserView.as_view(),name="UserPage"),
    path('user/detail', views.UserEditView.as_view(),name="UserEditPage"),
    path('user/reservationsManager',views.ReservationManagerView.as_view(), name="ReservationsManager"),
    path('user/reservationsManager/reservation_id=<int:reservation_id>',views.ReservationManagerView.as_view(),
         name="ReservationsManager_POST"),
    path('user/permissionManager', views.UserPermissionsPanelView.as_view(), name="PermissionsManager"),
    path('user/classManager',views.ClassManager.as_view(), name="ClassManager"),
    path('user/dormReservationsManager', views.DormReservationManagerView.as_view(), name="DormReservationsManager"),
    path('user/dormReservationsManager/reservation_id=<int:reservation_id>', views.DormReservationManagerView.as_view(),
         name="DormReservationsManager_POST"),
    path('user/classroomManager',views.ClassroomManager.as_view(),name="ClasroomManager")

]
