# Generated by Django 3.0.3 on 2020-03-07 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20200307_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, upload_to='recipes/static/'),
        ),
    ]
