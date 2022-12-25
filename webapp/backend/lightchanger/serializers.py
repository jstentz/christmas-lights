
# import serializers from the REST framework
from rest_framework import serializers
 
# import the todo data model
from .models import LightPatternOption, LightPattern
 
# create a serializer class
class LightOptionSerializer(serializers.ModelSerializer):
 
    # create a meta class
    class Meta:
        model = LightPatternOption
        fields = ('id', 'title','description','image_url')


class LightPatternSerializer(serializers.ModelSerializer):
 
    # create a meta class
    class Meta:
        model = LightPattern
        fields = ('id', 'light_pattern_id', 'timestamp')