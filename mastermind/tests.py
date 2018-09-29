from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from django.test import TestCase
from django.urls import reverse
from .models import Game, Color
from .services import GameFactory

class ViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.game_create_data = {}
        self.response = self.client.post(reverse('create'), self.game_create_data, format = 'json')

    def test_api_can_create_a_game(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_a_game(self):
        game = Game.objects.get()
        response = self.client.get(reverse('details', kwargs = {'pk': game.id}), format = 'json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)

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