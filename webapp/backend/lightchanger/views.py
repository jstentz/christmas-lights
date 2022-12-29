from django.shortcuts import render
from django.views.generic.base import View
from lightchanger.models import LightPattern, LightPatternOption
from lightchanger.serializers import LightOptionSerializer, LightPatternSerializer
from django.http import HttpResponseRedirect
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from functools import wraps
import json, requests


def is_request_authenticated(request):
  return settings.API_AUTH is None or (settings.API_AUTH_KEY in request.headers and request.headers[settings.API_AUTH_KEY] == settings.API_AUTH)

# Basic decorator that performs incredibly basic authentication for api views. 
# It only allows requests through that contain the correct secret in their headers.
# Otherwise, it returns 401.
def basic_authentication(func):
  @wraps(func)
  def wrapper(self, request, *args, **kwargs):
    if not is_request_authenticated(request):
      return Response(status=401)
    else:
      return func(self, request, *args, **kwargs)
  return wrapper

# Create your views here.
class HomePage(View):
    def get(self, request):
        pass
        # light_patterns = LightPatternOption.objects.all()
        # for lp in light_patterns:
        #     print(lp.title)
        #     print(lp.description)
        #     print(lp.image_url)
        #     print()
        # #context["light_patterns"] = light_patterns 
        # #return render(request, 'index.html', context)
        return HttpResponseRedirect("/")


class SelectLights(View):
    def get(self, request):
        print(request)
        return HttpResponseRedirect("/")
    def post(self, request):
        print(request)
        # send the info the raspberry pi somehow??? 
        new_light_pattern = LightPattern()
        #save to database so we can keep track of things
        new_light_pattern.save()
        return HttpResponseRedirect("/")


class LightOptionsView(viewsets.ReadOnlyModelViewSet):
    serializer_class = LightOptionSerializer
    queryset = LightPatternOption.objects.all()

    @basic_authentication
    def list(self, request, *args, **kwargs):
      return super().list(request, *args, **kwargs)

    @basic_authentication
    def retrieve(self, request, *args, **kwargs):
       return super().retrieve(request, *args, **kwargs)


class LightPatternsView(viewsets.ModelViewSet):
    serializer_class = LightPatternSerializer
    queryset = LightPattern.objects.all()

    @basic_authentication
    def list(self, request, *args, **kwargs):
      return super().list(request, *args, **kwargs)

    @basic_authentication
    def retrieve(self, request, *args, **kwargs):
       return super().retrieve(request, *args, **kwargs)

    @basic_authentication
    def create(self, request, *args, **kwargs):
       return super().create(request, *args, **kwargs)

    @basic_authentication
    def update(self, request, *args, **kwargs):
       return super().update(request, *args, **kwargs)
    
    @basic_authentication
    def destroy(self, request, *args, **kwargs):
       return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['GET'], name='Get last selected light pattern')
    @basic_authentication
    def last(self, request, *args, **kwargs):         
        queryset = LightPattern.objects.last()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'], name='Send most recent light pattern to raspberry pi.')
    @basic_authentication
    def updatepi(self, request, *args, **kwargs):
        light_pattern_json = json.dumps(request.data)
        print(light_pattern_json)
        requests.post(settings.LIGHTS_CONTROLLER_ENDPOINT, light_pattern_json, headers={'Content-Type': 'application/json'})
        return Response(status=200)
