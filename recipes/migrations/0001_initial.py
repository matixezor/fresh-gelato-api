# Generated by Django 3.0.3 on 2020-03-06 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Percentage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('percentage', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('base_amount', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Ingredient')),
                ('percentage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Percentage')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Recipe')),
            ],
        ),
    ]
