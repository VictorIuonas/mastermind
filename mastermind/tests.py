from rest_framework.test import APITestCase, APIRequestFactory
from .models import Game
from .views import GameViewSet

class TestGame(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = GameViewSet.as_view({'get': 'list'})
        self.uri = '/games/'

    def test_list(self):
        request = self.factory.get(self.uri)
        response = self.view(request)
        self.assertEqual(response.status_code, 200, 'Expected Response Code 200, received {} instead.'.format(response.status_code))

