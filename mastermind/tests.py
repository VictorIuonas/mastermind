from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Game, Color, Attempt, ResultColor
from .serializers import ColorConverter
from .services import GameFactory, AttemptResponseCalculator
from .views import CreateGameView

def convert_game_to_attempt_data(game):
    converter = ColorConverter()
    result = {
        'peg1': converter.from_color(game.peg1), 
        'peg2': converter.from_color(game.peg2), 
        'peg3': converter.from_color(game.peg3), 
        'peg4': converter.from_color(game.peg4),
    }

    return result

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

class CreateAttemptTestCase(TestCase):
    def setUp(self):
        self.color_converter = ColorConverter()
        self.base_scenario = CreateGameViewTestCase()
        self.base_scenario.setUp()
        self.client = self.base_scenario.client

        self.game_id = self.base_scenario.response.data['id']
        self.create_attempt_url = reverse('create_attempt', args = (self.game_id,))

        self.input_peg1 = Color.Red
        self.input_peg2 = Color.Blue
        self.input_peg3 = Color.Green
        self.input_peg4 = Color.Yellow

        self.create_attempt_data = {
            'peg1': self.color_converter.from_color(self.input_peg1), 
            'peg2': self.color_converter.from_color(self.input_peg2), 
            'peg3': self.color_converter.from_color(self.input_peg3), 
            'peg4': self.color_converter.from_color(self.input_peg4)
        }

        self.create_attempt_response = self.client.post(self.create_attempt_url, self.create_attempt_data, format = 'json')
    
    def test_api_can_create_an_attempt(self):
        self.assertEqual(self.create_attempt_response.status_code, status.HTTP_201_CREATED)

    def test_api_will_return_response(self):
        self.assertTrue("response1" in self.create_attempt_response.data)
        self.assertTrue("response2" in self.create_attempt_response.data)
        self.assertTrue("response3" in self.create_attempt_response.data)
        self.assertTrue("response4" in self.create_attempt_response.data)

class DetailsViewTestCase(TestCase):
    def setUp(self):
        self.color_converter = ColorConverter()
        self.base_scenario = CreateAttemptTestCase()
        self.base_scenario.setUp()
        self.client = self.base_scenario.client

        self.game_id = self.base_scenario.game_id
        self.game = Game.objects.get(id = self.game_id)

        self.create_second_attempt_data = convert_game_to_attempt_data(self.game)
        self.client.post(self.base_scenario.create_attempt_url, self.create_second_attempt_data, format = 'json')
        
        get_details_url = reverse('details', args = [self.game_id])

        self.game_details_response = self.client.get(get_details_url)

    def test_can_get_game_details(self):
        self.assertEqual(self.game_details_response.status_code, status.HTTP_200_OK)

    def test_details_contains_history_of_both_attempts(self):
        self.assertTrue('attempts' in self.game_details_response.data)
        game_history = self.game_details_response.data['attempts']
        self.assertEqual(len(game_history), 2)
        attempt1 = game_history[0]
        self.assertTrue('input' in attempt1)
        self.assertTrue('result' in attempt1)
        attempt2 = game_history[1]
        self.assertTrue('input' in attempt2)
        self.assertTrue('result' in attempt2)

    def test_details_contains_the_first_attempt(self):
        attempt1 = self.game_details_response.data['attempts'][0]
        self.assertEqual(self.color_converter.to_color(attempt1['input']['peg1']), self.base_scenario.input_peg1)
        self.assertEqual(self.color_converter.to_color(attempt1['input']['peg2']), self.base_scenario.input_peg2)
        self.assertEqual(self.color_converter.to_color(attempt1['input']['peg3']), self.base_scenario.input_peg3)
        self.assertEqual(self.color_converter.to_color(attempt1['input']['peg4']), self.base_scenario.input_peg4)

    def test_details_contains_the_second_attempt(self):
        attempt2 = self.game_details_response.data['attempts'][1]
        self.assertEqual(self.color_converter.to_color(attempt2['input']['peg1']), self.game.peg1)
        self.assertEqual(self.color_converter.to_color(attempt2['input']['peg2']), self.game.peg2)
        self.assertEqual(self.color_converter.to_color(attempt2['input']['peg3']), self.game.peg3)
        self.assertEqual(self.color_converter.to_color(attempt2['input']['peg4']), self.game.peg4)

    def test_details_contains_the_second_attempt_result(self):
        attempt2 = self.game_details_response.data['attempts'][1]
        self.assertEqual(attempt2['result']['response1'], str(ResultColor.Black))
        self.assertEqual(attempt2['result']['response2'], str(ResultColor.Black))
        self.assertEqual(attempt2['result']['response3'], str(ResultColor.Black))
        self.assertEqual(attempt2['result']['response4'], str(ResultColor.Black))

class MissingGameDetailsViewResultTestCase(TestCase):
    def setUp(self):
        self.base_scenario = CreateGameViewTestCase()
        self.base_scenario.setUp()
        self.client = self.base_scenario.client
        self.missing_game_id = 1000

        get_details_url = reverse('details', args = [self.missing_game_id])
        self.game_details_response = self.client.get(get_details_url)

    def test_get_details_for_missing_game_will_return_404(self):
        self.assertEqual(self.game_details_response.status_code, status.HTTP_404_NOT_FOUND)
    

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

class AttemptResponseCalculatorTestCase(TestCase):

    def setUp(self):
        self.calculator = AttemptResponseCalculator()
        self.game = Game()
        self.game.peg1 = Color.Blue
        self.game.peg2 = Color.Green
        self.game.peg3 = Color.Magenta
        self.game.peg4 = Color.Purple
        self.attempt = Attempt()
        self.attempt.game = self.game

    def test_calculator_returns_empty_response_for_an_attempt_not_matching_any(self):
        self.attempt.peg1 = Color.Red
        self.attempt.peg2 = Color.Yellow
        self.attempt.peg3 = Color.Blue
        self.attempt.peg4 = Color.Green

        response = self.calculator.calculate(self.attempt)
        
        self.assertEqual(response.response1, None)
        self.assertEqual(response.response2, None)
        self.assertEqual(response.response3, ResultColor.White)
        self.assertEqual(response.response4, ResultColor.White)

    def test_calculator_returns_response_for_all_pegs_in_attempt_matching_the_solution(self):
        self.attempt.peg1 = self.game.peg1
        self.attempt.peg2 = self.game.peg2
        self.attempt.peg3 = self.game.peg3
        self.attempt.peg4 = self.game.peg4

        response = self.calculator.calculate(self.attempt)

        self.assertEqual(response.response1, ResultColor.Black)
        self.assertEqual(response.response2, ResultColor.Black)
        self.assertEqual(response.response3, ResultColor.Black)
        self.assertEqual(response.response4, ResultColor.Black)
        
