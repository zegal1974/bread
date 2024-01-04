# Generated by Django 5.0 on 2023-12-24 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='movies',
            field=models.ManyToManyField(through='api.GenresMovies', to='api.movie'),
        ),
    ]