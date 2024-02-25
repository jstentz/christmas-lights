from django.shortcuts import render
from django.views.generic.base import View
from lightchanger.models import LightPattern, LightPatternOption, GeneratedAnimation
from lightchanger.serializers import LightOptionSerializer, LightPatternSerializer, GeneratedAnimationSerializer
from django.http import HttpResponseRedirect
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import HttpRequest
from django.conf import settings
from functools import wraps
import json, requests
from openai import OpenAI
import marko

client = OpenAI(api_key=settings.OPENAI_API_KEY)

from lights.animations import NAME_TO_ANIMATION


def is_request_authenticated(request):
  return settings.API_AUTH is None or (settings.API_AUTH_HEADER in request.headers and request.headers[settings.API_AUTH_HEADER] in settings.API_AUTH)

def is_admin_request_authenticated(request):
  return settings.ADMIN_API_AUTH is None or (settings.API_AUTH_HEADER in request.headers and request.headers[settings.API_AUTH_HEADER] in settings.ADMIN_API_AUTH)

# Basic decorator that performs incredibly basic authentication for api views. 
# It only allows requests through that contain the correct secret in their headers.
# Otherwise, it returns 401.
def basic_authentication(func):
  @wraps(func)
  def wrapper(self, request, *args, **kwargs):
    if not is_request_authenticated(request):
      return Response(status=401, data="Unauthorized: Make sure you've scanned the qr-code at the base of the tree.")
    else:
      return func(self, request, *args, **kwargs)
  return wrapper

def admin_authentication(func):
  @wraps(func)
  def wrapper(self, request, *args, **kwargs):
    if not is_admin_request_authenticated(request):
       return Response(status=401, data="Unauthorized")
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


class LightOptionsView(viewsets.ModelViewSet):
    serializer_class = LightOptionSerializer
    queryset = LightPatternOption.objects.all().order_by('position')

    def list(self, request, *args, **kwargs):
      return super().list(request, *args, **kwargs)

    @admin_authentication
    def retrieve(self, request, *args, **kwargs):
       return super().retrieve(request, *args, **kwargs)

    @admin_authentication
    def create(self, request, *args, **kwargs):
       return super().create(request, *args, **kwargs)

    @admin_authentication
    def update(self, request, *args, **kwargs):
       return super().update(request, *args, **kwargs)
    
    @admin_authentication
    def destroy(self, request, *args, **kwargs):
       return super().destroy(request, *args, **kwargs)

    @admin_authentication
    def partial_update(self, request, *args, **kwargs):
       return super().partial_update(request, *args, **kwargs)

    @action(detail=False, methods=['POST'], name='Validate new animation parameters')
    @basic_authentication
    def reset_parameters(self, request, *args, **kwargs):
      light_pattern_json = request.data
      light_pattern_id = light_pattern_json['light_pattern_id']
      existing = LightPatternOption.objects.get(pk=light_pattern_id)
      light_pattern_name = existing.animation_id
      
      animation = NAME_TO_ANIMATION[light_pattern_name]()

      default_parameters = animation.get_default_parameters()
      existing.parameters_json = animation.serialize_parameters(default_parameters)
      existing.default_parameters_json = existing.parameters_json
      existing.save()
      
      return Response(200)

    @action(detail=False, methods=['POST'], name='Validate and update new animation parameters')
    @basic_authentication
    def update_parameters(self, request, *args, **kwargs):
      light_pattern_json = request.data
      light_pattern_id = light_pattern_json['light_pattern_id']
      new_parameters = light_pattern_json['parameters']
      existing = LightPatternOption.objects.get(pk=light_pattern_id)
      light_pattern_name = existing.animation_id
      
      animation = NAME_TO_ANIMATION[light_pattern_name]()

      try:
        parameters = animation.deserialize_parameters(new_parameters)
      except json.JSONDecodeError:
        return Response(data="invalid input format", status=400)

      try:
        animation.validate_parameters(parameters)
      except TypeError as e:
        return Response(data=str(e), status=400)

      existing.parameters_json = new_parameters
      existing.save()
      
      return Response(200)

class LightPatternsView(viewsets.ModelViewSet):
    serializer_class = LightPatternSerializer
    queryset = LightPattern.objects.all()

    @admin_authentication
    def list(self, request, *args, **kwargs):
      return super().list(request, *args, **kwargs)

    @admin_authentication
    def retrieve(self, request, *args, **kwargs):
       return super().retrieve(request, *args, **kwargs)

    @admin_authentication
    def create(self, request, *args, **kwargs):
       return super().create(request, *args, **kwargs)

    @admin_authentication
    def update(self, request, *args, **kwargs):
       return super().update(request, *args, **kwargs)
    
    @admin_authentication
    def destroy(self, request, *args, **kwargs):
       return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['GET'], name='Get last selected light pattern')
    def last(self, request, *args, **kwargs):         
        queryset = LightPattern.objects.last()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'], name='Send most recent light pattern to raspberry pi')
    @basic_authentication
    def updatepi(self, request, *args, **kwargs):
        light_pattern_id = request.data['light_pattern_id']
        light_pattern = LightPatternOption.objects.get(pk=light_pattern_id)
        light_pattern_name = light_pattern.animation_id

        animation = NAME_TO_ANIMATION[light_pattern_name]()
        parameters = animation.deserialize_parameters(light_pattern.parameters_json)

        try:
          animation.validate_parameters(parameters)
        except TypeError as e:
          return Response(data=str(e), status=400)

        update_payload = {
           'light_pattern_name': light_pattern_name,
           'parameters': parameters
        }
        update_payload_json = json.dumps(update_payload)

        requests.post(settings.LIGHTS_CONTROLLER_ENDPOINT, update_payload_json, headers={'Content-Type': 'application/json'})
        return Response(status=200)

class GeneratedAnimationsView(viewsets.GenericViewSet):
   serializer_class = GeneratedAnimationSerializer
   queryset = GeneratedAnimation.objects.all()

   # assumes the relevant code is located at the root of the document, is not nested inside another element, and is formatted as a 'FencedCode' element.
   def _extract_code(self, model_response: str) -> str:
      md = marko.Markdown()
      parsed_markdown = md.parse(model_response)
      code_blocks = [n for n in parsed_markdown.children if n.get_type() == 'FencedCode']
      return code_blocks[0].children[0].children


   @action(detail=False, methods=['POST'], name='Generate a new animation from a prompt using AI')
   @admin_authentication
   def generate(self, request, *args, **kwargs):
      prompt = request.data['prompt']
      if len(prompt) > settings.MAX_PROMPT_LENGTH:
         return Response(status=400, data="Error: prompt too long")
      generated_animation_entry = GeneratedAnimation(prompt=prompt, title="", author="", generated_animation="")

      response = client.chat.completions.create(
         model="gpt-4-turbo-preview",
         messages=[
            {"role": "system", "content": settings.SYSTEM_MESSAGE},
            {"role": "user", "content": prompt}
         ],
      )

      generated_animation_entry.model_response = response.choices[0].message.content
      try:
         extracted_code = self._extract_code(generated_animation_entry.model_response)
      except:
         extracted_code = response.choices[0].message.content
      generated_animation_entry.generated_animation = extracted_code
      generated_animation_entry.save()
      
      return Response(status=200, data=generated_animation_entry.pk)
   
   @action(detail=False, methods=['POST'], name='Preview a generated animation on the tree')
   @admin_authentication
   def preview(self, request, *args, **kwargs):
      generated_animation_id = request.data['generated_animation_id']
      generated_animation_entry = GeneratedAnimation.objects.get(pk=generated_animation_id)

      preview_payload = {
         'generated_animation': generated_animation_entry.generated_animation
      }

      preview_payload_json = json.dumps(preview_payload)
      res = requests.post(settings.LIGHTS_CONTROLLER_ENDPOINT + '/preview', preview_payload_json, headers={'Content-Type': 'application/json'})
      return Response(status=res.status_code)
   
   # TODO: Will need an update function or some way of adding in the author's name to the generated animation.