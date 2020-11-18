from django.urls import path
from . import views
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('api/users', UzytkownikView, 'users')

urlpatterns = router.urls