from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Game, Color
from .services import GameFactory
from .views import CreateGameView

class ApiClientAuthenticator():
    def __init__(self):
        self.username = 'test'
        self.email = 'john@doe.com'
        self.password = '123'

        User.objects.create(username = self.username, email = self.email, password = self.password)
        self.user = User.objects.get(username = 'test')
    
    def authenticate(self, apiClient):
        apiClient.force_authenticate(user = self.user)

class CreateGameViewTestCase(APITestCase):
    def setUp(self):
        self.authenticator = ApiClientAuthenticator()
        self.client = APIClient()
        self.authenticator.authenticate(self.client)
        self.game_create_data = {}
        self.response = self.client.post(reverse('create'), self.game_create_data, format = 'json')

    def test_api_can_create_a_game(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_a_game(self):
        game = Game.objects.get()
        response = self.client.get(reverse('details', kwargs = {'pk': game.id}), format = 'json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)

class CreateAttemptTestCase(TestCase):
    def setUp(self):
        self.base_scenario = CreateGameViewTestCase()
        self.base_scenario.setUp()

        self.game_id = self.base_scenario.response.data['id']
        create_attempt_url = reverse('create_attempt', args = (self.game_id,))
        
        self.create_attempt_data = {'peg1': 'R', 'peg2': 'B', 'peg3': 'G', 'peg4': 'Y'}
        self.create_attempt_response = self.base_scenario.client.post(create_attempt_url, self.create_attempt_data, format = 'json')
    
    def test_api_can_create_an_attempt(self):
        self.assertEqual(self.create_attempt_response.status_code, status.HTTP_201_CREATED)

class ModelTestCase(TestCase):

    def setUp(self):
        self.game = Game()
        self.game.peg1 = Color.Blue
        self.game.peg2 = Color.Red
        self.game.peg3 = Color.Yellow
        self.game.peg4 = Color.Green

    def test_model_can_create_a_game(self):
        old_game_count = Game.objects.count()

        self.game.save()

        new_game_count = Game.objects.count()

        self.assertEqual(old_game_count + 1, new_game_count)
        self.assertEqual(self.game.peg1, Color.Blue)
        self.assertEqual(self.game.peg2, Color.Red)
        self.assertEqual(self.game.peg3, Color.Yellow)
        self.assertEqual(self.game.peg4, Color.Green)

    def test_game_solution_choice(self):
        print('all colors: ', list(Color))

class SolutionGeneratorTestCase(TestCase):

    def setUp(self):
        self.factory = GameFactory()

    def test_game_is_created_with_random_colors(self):
        game = self.factory.create()

        self.assertFalse(game.peg1 == game.peg2 == game.peg3 == game.peg4)