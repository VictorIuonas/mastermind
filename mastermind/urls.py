from django.conf.urls import url, include
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import GameViewSet, CreateView, DetailsView

#router = DefaultRouter()
#router.register('games', GameViewSet, base_name = 'games')

urlpatterns = [
    url(r'^game/$', CreateView.as_view(), name = 'create'),
    url(r'game/(?P<pk>[0-9]+)/$', DetailsView.as_view(), name = 'details')
]

#urlpatterns += router.urls
