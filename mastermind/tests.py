from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from django.test import TestCase
from django.urls import reverse
from .models import Game
from .views import GameViewSet

class ViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.game_create_data = {}
        self.response = self.client.post(reverse('create'), self.game_create_data, format = 'json')

    def test_api_can_create_a_game(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_a_game(self):
        print('the can get a game test')

        game = Game.objects.get()
        response = self.client.get(reverse('details', kwargs = {'pk': game.id}), format = 'json')

        print('get by id response: ', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)

class ModelTestCase(TestCase):

    def setUp(self):
        self.game = Game()

    def test_model_can_create_a_game(self):
        old_count = Game.objects.count()
        self.game.save()
        new_count = Game.objects.count()
        self.assertEqual(old_count + 1, new_count)

