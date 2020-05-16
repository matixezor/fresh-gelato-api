from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Recipe, RecipeIngredient, Ingredient, Email


class RecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='ingredient.name')
    price = serializers.FloatField(source='ingredient.price')
    amount = serializers.SerializerMethodField()
    cost = serializers.SerializerMethodField()

    class Meta:
        model = RecipeIngredient
        fields = ['name', 'amount', 'price', 'cost', 'percentage']

    def get_amount(self, obj):
        return round(obj.recipe.base_amount * obj.percentage)

    def get_cost(self, obj):
        return round(obj.ingredient.price * self.get_amount(obj) / 1000, 2)


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True)
    total_price = serializers.SerializerMethodField()
    ingredient_count = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'base_amount', 'total_price', 'image', 'ingredient_count', 'ingredients']

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)

        for ingredients_data in ingredients_data:
            ingredient, created = Ingredient.objects.get_or_create(
                name=ingredients_data['ingredient']['name'],
                price=ingredients_data['ingredient']['price']
            )

            RecipeIngredient.objects.create(
                recipe=recipe,
                percentage=ingredients_data['percentage'],
                ingredient=ingredient
            )
        return recipe

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
