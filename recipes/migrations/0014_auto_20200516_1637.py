# Generated by Django 3.0.3 on 2020-05-16 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0013_auto_20200516_1635'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='recipeingredient',
            unique_together={('recipe', 'ingredient')},
        ),
    ]
