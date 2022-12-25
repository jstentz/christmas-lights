from django.shortcuts import render
from django.views.generic.base import View
from lightchanger.models import LightPattern, LightPatternOption
from lightchanger.serializers import LightOptionSerializer, LightPatternSerializer
from django.http import HttpResponseRedirect
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response



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


class LightOptionsView(viewsets.ModelViewSet):
    serializer_class = LightOptionSerializer
    queryset = LightPatternOption.objects.all()


class LightPatternsView(viewsets.ModelViewSet):
    serializer_class = LightPatternSerializer
    queryset = LightPattern.objects.all()

    @action(detail=False, methods=['GET'], name='Get last selected light pattern')
    def last(self, request, *args, **kwargs):
        queryset = LightPattern.objects.last()

        serializer = self.get_serializer(queryset)
        return Response(serializer.data)
