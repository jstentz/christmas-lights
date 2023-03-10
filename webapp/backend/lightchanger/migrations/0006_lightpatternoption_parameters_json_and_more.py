# Generated by Django 4.1.4 on 2023-01-21 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lightchanger', '0005_lightpatternoption_animation_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='lightpatternoption',
            name='parameters_json',
            field=models.JSONField(default={}),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lightpatternoption',
            name='image_url',
            field=models.TextField(null=True),
        ),
    ]
