from django.urls import path
from . import views
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('api/users', UzytkownikView, 'users')
router.register('api/wydzialy',WydzialView,'wydzialy')
router.register('api/kierunki',KierunekView,'kierunki')
router.register('api/studenci',StudentView,'studenci')
router.register('api/rezerwacje_sal',RezerwacjaSaliView,'rezerwacje_sal')
router.register('api/pracownie_specjalistyczne',PracowniaSpecjalistycznaView,'pracownie_specjalistyczne')
router.register('api/sale',SalaView,'sale')
router.register('api/laboratoria',LaboratoriumView,'laboratoria')

urlpatterns = router.urls