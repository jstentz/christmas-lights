from django.contrib import admin
from .models import LightPattern, LightPatternOption

# Register your models here.

class LightPatternAdmin(admin.ModelAdmin):
    list_display = ('light_pattern_id', 'timestamp')

class LightPatternOptionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'image_url')


admin.site.register(LightPattern, LightPatternAdmin)
admin.site.register(LightPatternOption, LightPatternOptionAdmin)
