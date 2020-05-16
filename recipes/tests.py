from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from .serializers import RecipeListSerializer, RecipeSerializer, UserSerializer
from .models import Recipe
import json


class CurrentUserTest(APITestCase):

    def setUp(self):
        User.objects.create(username="test", password=make_password("test1234!"))

    def test_authorization(self):
        res = self.client.post('/api/token-auth/', {"username": "test", "password": "test1234!"})
        self.assertEqual(200, res.status_code)

        res = self.client.post('/api/token-auth/', {"username": "test", "password": "tdsa"})
        self.assertEqual(400, res.status_code)

    def test_get_valid_curr_user(self):
        res = self.client.post('/api/token-auth/', {"username": "test", "password": "test1234!"})
        res = json.loads(res.content)
        token = res['token']

        res = self.client.get('/api/current-user/', {}, HTTP_AUTHORIZATION=f'JWT {token}')

        serializer = UserSerializer(User.objects.get(username="test"))

        self.assertEqual(200, res.status_code)
        self.assertEqual(serializer.data, res.data)

    def test_get_invalid_curr_user(self):
        res = self.client.get('/api/current-user/', {}, HTTP_AUTHORIZATION=f'JWT 1452512512')

        self.assertEqual(401, res.status_code)


class RecipeTests(APITestCase):

    def setUp(self):
        User.objects.create(username="test", password=make_password("test1234!"))
        res = self.client.post('/api/token-auth/', {"username": "test", "password": "test1234!"})
        res = json.loads(res.content)

        Recipe.objects.create(name="Czekolada", base_amount="123")
        Recipe.objects.create(name="Mieta", base_amount="243")

        self.token = res['token']

    def test_get_recipes_list(self):
        res = self.client.get('/api/recipes/', {}, HTTP_AUTHORIZATION=f'JWT {self.token}')

        recipes = Recipe.objects.all()
        serializer = RecipeListSerializer(recipes, many=True)

        self.assertEqual(200, res.status_code)
        self.assertEqual(serializer.data, res.data)

    def test_get_valid_recipe(self):
        res = self.client.get('/api/recipes/1/', {}, HTTP_AUTHORIZATION=f'JWT {self.token}')

        recipe = Recipe.objects.get(id=1)
        serializer = RecipeSerializer(instance=recipe)

        self.assertEqual(200, res.status_code)
        self.assertEqual(serializer.data, res.data)

    def test_get_invalid_recipe(self):
        res = self.client.get('/api/recipes/2543/', {}, HTTP_AUTHORIZATION=f'JWT {self.token}')

        self.assertEqual(404, res.status_code)


