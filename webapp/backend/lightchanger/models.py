from django.db import models

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
