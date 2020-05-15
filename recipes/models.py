from django.db import models


class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    base_amount = models.IntegerField()
    image = models.ImageField(upload_to='', blank=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    price = models.FloatField()

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)
    percentage = models.FloatField()
    ingredient = models.ForeignKey(Ingredient, related_name='ingredient', on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.recipe.name} - {self.ingredient.name}'


class Email(models.Model):
    sender_name = models.CharField(max_length=50)
    sender_mail = models.EmailField(max_length=50)
    content = models.CharField(max_length=500)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender_mail} - {self.date}'