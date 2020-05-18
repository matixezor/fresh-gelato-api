from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from .serializers import RecipeListSerializer, RecipeSerializer, UserSerializer
from .models import Recipe
import json


class UserTest(APITestCase):

    def setUp(self):
        User.objects.create(username="test", password=make_password("test1234!"))

        res = self.client.post('/api/token-auth/', {"username": "test", "password": "test1234!"})
        res = json.loads(res.content)
        self.token = res['token']
        self.valid_user = {
            "username": "Karol",
            "first_name": "Karol",
            "last_name": "Nowak",
            "email": "123@example.pl",
            "password": "Test1234!"
        }

        self.invalid_user = {
            "username": "invalid_user",
            "email": "123@example.pl"
        }

    def test_valid_authorization(self):
        res = self.client.post('/api/token-auth/', {"username": "test", "password": "test1234!"})
        self.assertEqual(200, res.status_code)

    def test_invalid_authorization(self):
        res = self.client.post('/api/token-auth/', {"username": "test", "password": "tdsa"})
        self.assertEqual(400, res.status_code)

    def test_get_valid_curr_user(self):
        res = self.client.get('/api/user/', {}, HTTP_AUTHORIZATION=f'JWT {self.token}')
        self.assertEqual(200, res.status_code)

        serializer = UserSerializer(User.objects.get(username="test"))
        self.assertEqual(serializer.data, res.data)

    def test_post_valid_user(self):
        res = self.client.post('/api/user/', self.valid_user)
        self.assertEqual(201, res.status_code)

        serializer = UserSerializer(User.objects.get(username="Karol"))
        del self.valid_user['password']

        self.assertEqual(serializer.data, self.valid_user)

    def test_post_invalid_user(self):
        res = self.client.post('/api/user/', self.invalid_user)
        self.assertEqual(400, res.status_code)

    def test_invalid_request_method(self):
        res = self.client.put('/api/user/', {})
        self.assertEqual(405, res.status_code)

    def test_get_invalid_curr_user(self):
        res = self.client.get('/api/user/', {}, HTTP_AUTHORIZATION=f'JWT 1452512512')
        self.assertEqual(401, res.status_code)


class RecipeTests(APITestCase):

    def setUp(self):
        User.objects.create(username="test", password=make_password("test1234!"), is_staff=True)
        res = self.client.post('/api/token-auth/', {"username": "test", "password": "test1234!"})
        res = json.loads(res.content)

        self.token = res['token']

        Recipe.objects.create(name="Czekolada", base_amount="123")
        Recipe.objects.create(name="Mieta", base_amount="243")

        self.valid_data = {
            "name": "Lody sorbet malina",
            "base_amount": 12412,
            "ingredients": [
                {
                    "name": "Baza Mleczna Natural Milk Base GX",
                    "price": 25.34,
                    "percentage": 0.187
                },
                {
                    "name": "Pasta orzech ziemny",
                    "price": 23.41,
                    "percentage": 0.082
                }
            ]
        }

        self.invalid_data = {
            "name": "Lody sorbet malina",
            "base_amount": "dsad",
            "ingredients": ""
        }

    def test_get_recipes_list(self):
        res = self.client.get('/api/recipes/', {}, HTTP_AUTHORIZATION=f'JWT {self.token}')
        self.assertEqual(200, res.status_code)

        recipes = Recipe.objects.all()
        serializer = RecipeListSerializer(recipes, many=True)

        self.assertEqual(serializer.data, res.data)

    def test_post_valid_recipe(self):
        res = self.client.post('/api/recipes/', self.valid_data, format='json', HTTP_AUTHORIZATION=f'JWT {self.token}')
        self.assertEqual(201, res.status_code)

        recipe = Recipe.objects.get(name="Lody sorbet malina")
        serializer = RecipeSerializer(instance=recipe)
        """
        need to exclude id from serializer.data, as sent data doesn't contain id
        same goes for all the new fields that are calculated server-side in serializers
        """
        keys_to_remove = ['id', 'total_price', 'image', 'ingredient_count']
        serializer = serializer.data
        for key in keys_to_remove:
            del serializer[key]
        for ingredient in serializer['ingredients']:
            del ingredient['amount']
            del ingredient['cost']

        self.assertEqual(serializer, self.valid_data)

    def test_post_invalid_recipe(self):
        res = self.client.post('/api/recipes/', self.invalid_data, format='json',
                               HTTP_AUTHORIZATION=f'JWT {self.token}')
        self.assertEqual(400, res.status_code)

        res = self.client.post('/api/recipes/', {}, HTTP_AUTHORIZATION=f'JWT {self.token}')
        self.assertEqual(400, res.status_code)

    def test_get_valid_recipe(self):
        res = self.client.get('/api/recipes/1/', {}, HTTP_AUTHORIZATION=f'JWT {self.token}')
        self.assertEqual(200, res.status_code)

        recipe = Recipe.objects.get(id=1)
        serializer = RecipeSerializer(instance=recipe)

        self.assertEqual(serializer.data, res.data)

    def test_get_invalid_recipe(self):
        res = self.client.get('/api/recipes/2543/', {}, HTTP_AUTHORIZATION=f'JWT {self.token}')
        self.assertEqual(404, res.status_code)

        res = self.client.get('/api/recipes/das/', {}, HTTP_AUTHORIZATION=f'JWT {self.token}')
        self.assertEqual(404, res.status_code)
