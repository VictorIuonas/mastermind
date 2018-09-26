from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import GameViewSet

router = DefaultRouter()
router.register('games', GameViewSet, base_name = 'games')

urlpatterns = [
]

urlpatterns += router.urls
