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
from typing import Dict
import ast

client = OpenAI(api_key=settings.OPENAI_API_KEY)

from lights.animations import NAME_TO_ANIMATION
from lights.animations.base import BaseAnimation


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

    @basic_authentication
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
   

   def _get_init_func(self, parsed_animation: ast.Module) -> ast.FunctionDef | None:
    for node in parsed_animation.body:
      if isinstance(node, ast.ClassDef):
        for base in node.bases:
          if isinstance(base, ast.Name) and base.id == BaseAnimation.__name__:
            for child_node in node.body:
              if isinstance(child_node, ast.FunctionDef) and child_node.name == '__init__':
                return child_node
    return None


   # Assumes 1 and only 1 BaseAnimation child class is defined in the source file
   def _get_animation_parameters(self, animation_source: str) -> Dict | None:
     parsed = ast.parse(animation_source)
     
     init_function = self._get_init_func(parsed)
     if init_function is None:
       return None
     
     args = init_function.args
     return {arg.arg: json.dumps(ast.literal_eval(value)) for arg, value in zip(args.kwonlyargs, args.kw_defaults)}


   @action(detail=False, methods=['POST'], name='Generate a new animation from a prompt using AI')
   @admin_authentication
   def generate(self, request, *args, **kwargs):
      prompt = request.data['prompt']
      if len(prompt) > settings.MAX_PROMPT_LENGTH:
         return Response(status=400, data="Error: prompt too long")
      generated_animation_entry = GeneratedAnimation(prompt=prompt, title="", author="", generated_animation="", parameters_json=dict())

      response = client.chat.completions.create(
         model=settings.OPENAI_MODEL,
         messages=[
            {"role": "system", "content": settings.SYSTEM_MESSAGE},
            {"role": "user", "content": prompt}
         ],
      )

      print(response)

      generated_animation_entry.model_response = response.choices[0].message.content
      try:
         extracted_code = self._extract_code(generated_animation_entry.model_response)
      except:
         extracted_code = response.choices[0].message.content

      try:
         parameters = self._get_animation_parameters(extracted_code)
      except:
         parameters = {}
      
      generated_animation_entry.generated_animation = extracted_code
      generated_animation_entry.parameters_json = parameters
      generated_animation_entry.save()

      generated_animation_response = {
         'id': generated_animation_entry.pk,
         'parameters_json': parameters
      }
      
      return Response(status=200, data=json.dumps(generated_animation_response))
   
   @action(detail=False, methods=['POST'], name='Preview a generated animation on the tree')
   @admin_authentication
   def preview(self, request, *args, **kwargs):
      generated_animation_id = request.data['id']
      generated_animation_entry = GeneratedAnimation.objects.get(pk=generated_animation_id)

      parameters = BaseAnimation.deserialize_parameters(generated_animation_entry.parameters_json)

      preview_payload = {
         'generated_animation': generated_animation_entry.generated_animation,
         'parameters_json': parameters,
      }

      preview_payload_json = json.dumps(preview_payload)
      res = requests.post(settings.LIGHTS_CONTROLLER_ENDPOINT + '/preview', preview_payload_json, headers={'Content-Type': 'application/json'})
      return Response(status=res.status_code)
   
   @action(detail=False, methods=['POST'], name='Submit a generated animation for review')
   @admin_authentication
   def submit(self, request, *args, **kwargs):
      generated_animation_id = request.data['id']
      title = request.data['title']
      author = request.data['author']

      generated_animation_entry = GeneratedAnimation.objects.get(pk=generated_animation_id)
      if generated_animation_entry.author != "" or generated_animation_entry.title != "":
         return Response(status=400, data='Animation already submitted for review')
      
      generated_animation_entry.title = title
      generated_animation_entry.author = author
      generated_animation_entry.save()

      return Response(status=200)
   
   @action(detail=False, methods=['POST'], name='Update a generated animations parameters')
   @admin_authentication
   def update_parameters(self, request, *args, **kwargs):
      generated_animation_id = request.data['id']
      new_parameters = request.data['parameters_json']
      existing = GeneratedAnimation.objects.get(pk=generated_animation_id)
     
      existing.parameters_json = new_parameters
      
      existing.save()
      
      return Response(200)
   