
# import serializers from the REST framework
from rest_framework import serializers
 
# import the todo data model
from .models import LightPatternOption, LightPattern
 
# create a serializer class
class LightOptionSerializer(serializers.ModelSerializer):
 
    # create a meta class
    class Meta:
        model = LightPatternOption
        fields = ('id', 'position', 'title', 'description', 'image_url', 'animation_id', 'parameters_json')


class LightPatternSerializer(serializers.ModelSerializer):
 
    # create a meta class
    class Meta:
        model = LightPattern
        fields = ('id', 'light_pattern_id', 'timestamp')