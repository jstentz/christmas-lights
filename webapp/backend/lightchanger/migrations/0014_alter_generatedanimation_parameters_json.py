# Generated by Django 4.1.4 on 2024-02-29 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lightchanger', '0013_generatedanimation_parameters_json_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generatedanimation',
            name='parameters_json',
            field=models.JSONField(default=dict, null=True),
        ),
    ]
