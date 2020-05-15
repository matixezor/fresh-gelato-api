from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Recipe, RecipeIngredient, Email


class RecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='ingredient.name')
    price = serializers.FloatField(source='ingredient.price')
    amount = serializers.SerializerMethodField()
    cost = serializers.SerializerMethodField()

    class Meta:
        model = RecipeIngredient
        fields = ['name', 'amount', 'price', 'cost', 'percentage']

    def get_amount(self, obj):
        return round(obj.recipe.base_amount*obj.percentage)

    def get_cost(self, obj):
        return round(obj.ingredient.price*self.get_amount(obj)/1000, 2)


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True)
    total_price = serializers.SerializerMethodField()
    ingredient_count = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'base_amount', 'total_price', 'image', 'ingredient_count', 'ingredients']

    def get_total_price(self, obj):
        total_price = 0
        for ingredient in obj.ingredients.all():
            total_price += ingredient.ingredient.price
        return total_price

    def get_ingredient_count(self, obj):
        return obj.ingredients.all().count()


class RecipeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image']


class EmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Email
        fields = ['sender_name', 'sender_mail', 'content']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email']


