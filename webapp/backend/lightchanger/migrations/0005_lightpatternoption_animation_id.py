# Generated by Django 3.2.13 on 2022-12-27 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lightchanger', '0004_lightpatternoption_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='lightpatternoption',
            name='animation_id',
            field=models.TextField(default=''),
        ),
    ]
