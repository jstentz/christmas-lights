"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 3.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import json

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Basic Authorization:
API_AUTH_HEADER= 'API_AUTH'
API_AUTH_ENV = 'API_AUTH'
ADMIN_API_AUTH_ENV = 'ADMIN_API_AUTH'
if DEBUG:
  # SECURITY WARNING: keep the secret key used in production secret!
  SECRET_KEY = 'django-insecure-026(81kz90bga8ww%l)m=(co^5#fx*2$i7ml=dp_8&$5c^+$8%'
  API_AUTH = None
  ADMIN_API_AUTH = None
else:
  try:
    SECRET_KEY = os.environ['SECRET_KEY']
  except KeyError as e:
    raise RuntimeError("Running with DEBUG=False but couldn't find a SECRET_KEY in environment.") from e
  
  try:
    API_AUTH = json.loads(os.environ[API_AUTH_ENV])
  except KeyError as e:
    raise RuntimeError("Running with DEBUG=False but couldn't find an API_AUTH in environment.") from e
  
  try:
    ADMIN_API_AUTH = json.loads(os.environ[ADMIN_API_AUTH_ENV])
  except KeyError as e:
    raise RuntimeError("Running with DEBUG=False but couldn't find an ADMIN_API_ATH in environment.") from e

ALLOWED_HOSTS = [
  "lights.ryanstentz.com",
  "lights-staging.ryanstentz.com",
  "localhost",
  "127.0.0.1"
]

# Lights Controller Configuration:
LIGHTS_CONTROLLER_ENDPOINT = "http://192.168.1.25:8000/"

# Animation Generation Configuration:
MAX_PROMPT_LENGTH=1000
MAX_TITLE_LENGTH=30
MAX_AUTHOR_LENGTH=30
SYSTEM_MESSAGE = '''
# There is a tree outside wrapped in programmable lights. Given a user-supplied prompt and the template below, generate valid python code that animates these lights according to the prompt. 
# Do not use anything without either importing it or defining it. Keep the code concise, and don't add comments.

```
import numpy as np 
from typing import Optional, Collection
from lights.animations.base import BaseAnimation # this is the class that all animations should inherit from

class UniformColorLights(BaseAnimation): # All animations should inherit from the parent class 'BaseAnimation'
  """This is an example class for the light animation where all of the lights in the input frameBuf 
  will be set to red."""

  def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = None, color: Collection[int] = (255, 0, 0)):
    """
    Required:
    These parameters must be present in the __init__ function for all animation classes.
     - frameBuf [np.ndarray]: A Nx3 array of RGB color values where N is the number of lights  
     - fps [int | None]: The speed of the animation in frames per second 

    Optional:
    These keyword parameters are specific to this animation. Be creative and add these parameters to further customize the animation.
    - color [tuple[int]]: Desired color for the lights as RGB. The default is red.
    """
    super().__init__(frameBuf, fps) # Must be present
    self.color = color

  def renderNextFrame(self):
    """
    This function should generate the next animation frame and store in the class's frameBuf attribute. 

    IMPORTANT! The frameBuf is a shared buffer, so all modifications must be in place. Operations that create a copy of the frameBuf will not work. 
    """
    self.frameBuf[:] = self.color # this sets every color value in the frameBuf to the input color
```
'''
OPENAI_API_KEY_ENV = 'OPENAI_API_KEY'
try:
    OPENAI_API_KEY = os.environ[OPENAI_API_KEY_ENV]
except KeyError:
    print("WARNING: OPENAI_API_KEY was not found in your terminal environment variables. Endpoints that use OpenAI (e.g. /generate/generate) will not work")
    OPENAI_API_KEY = ""

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'lightchanger',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'backend', 'static', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ORIGIN_WHITELIST = [
     'http://localhost:3000'
]

CORS_ALLOW_HEADERS = [
    "API_AUTH",
    "content-type"
]

STATIC_URL = os.path.join(BASE_DIR, 'static/')

STATIC_ROOT = os.path.join(BASE_DIR, 'static_content/')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static/'),
)
