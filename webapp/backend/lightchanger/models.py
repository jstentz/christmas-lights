from django.db import models

# Create your models here.

class LightPatternOption(models.Model):
    title = models.TextField(max_length=100, default="")
    description = models.TextField(max_length=1000)
    image_url = models.URLField(null=True)
    animation_id = models.TextField(default="")

class LightPattern(models.Model):
    light_pattern_id = models.ForeignKey(LightPatternOption, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(null=True)



