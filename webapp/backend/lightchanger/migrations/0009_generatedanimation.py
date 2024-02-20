# Generated by Django 4.1.4 on 2024-02-19 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lightchanger', '0008_lightpatternoption_default_parameters_json'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneratedAnimation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prompt', models.TextField(max_length=150)),
                ('title', models.TextField(max_length=30)),
                ('author', models.TextField(max_length=30)),
                ('generated_animation', models.TextField()),
            ],
        ),
    ]