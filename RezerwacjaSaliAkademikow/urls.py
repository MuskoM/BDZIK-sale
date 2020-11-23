from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('reservations/', include("frontend.urls")),
    path('reservations/', include('reservations.urls')),
    path('reservations/', include('accounts.urls'))
]
