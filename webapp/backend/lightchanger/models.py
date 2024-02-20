from django.db import models
from django.conf import settings

# Create your models here.

class LightPatternOption(models.Model):
    title = models.TextField(max_length=100, default="")
    position = models.IntegerField(default=-1)
    description = models.TextField(max_length=1000)
    image_url = models.TextField(null=True)
    animation_id = models.TextField(default="")
    parameters_json = models.JSONField()
    default_parameters_json = models.JSONField()

class LightPattern(models.Model):
    light_pattern_id = models.ForeignKey(LightPatternOption, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(null=True)

class GeneratedAnimation(models.Model):
    prompt = models.TextField(max_length=settings.MAX_PROMPT_LENGTH)
    title = models.TextField(max_length=settings.MAX_TITLE_LENGTH)
    author = models.TextField(max_length=settings.MAX_AUTHOR_LENGTH)
    model_response = models.TextField(null=True, default="")
    generated_animation = models.TextField(null=True, default="")