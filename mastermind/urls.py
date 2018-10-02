from django.conf.urls import url, include
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CreateGameView, DetailsView, AttemptView

urlpatterns = [
    url(r'^game/$', CreateGameView.as_view(), name = 'create'),
    url(r'^game/(?P<pk>[0-9]+)/$', DetailsView.as_view(), name = 'details'),
    url(r'^game/(?P<game_id>[0-9]+)/attempt/$', AttemptView.as_view(), name = 'create_attempt'),
    path('rest-auth/', include('rest_auth.urls')),
]

#urlpatterns += router.urls
