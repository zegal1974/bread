# Generated by Django 5.0 on 2023-12-25 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_genre_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='magnet',
            name='hash',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='magnet',
            name='link',
            field=models.CharField(max_length=100, null=True),
        ),
    ]