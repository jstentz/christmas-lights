import argparse
import requests
import datetime
import random

API_ENDPOINT = 'https://lights.ryanstentz.com/api/'

def get_animations(api_auth):
  r = requests.get(API_ENDPOINT + '/options/', headers={'API_AUTH': api_auth})
  return {animation['animation_id']: animation for animation in r.json()}

def turn_off_lights(animations, api_auth):
  turn_on_animation(animations, 'Off', api_auth)

def turn_on_random(animations, api_auth):
  animation_name = 'Off'
  while animation_name == 'Off':
    animation_name = random.choice(list(animations.keys()))
  
  turn_on_animation(animations, animation_name, api_auth)

def turn_on_animation(animations, animation_name, api_auth):
  selection = {
    'light_pattern_id': animations[animation_name]['id'],
    'timestamp': datetime.datetime.now().isoformat()
  }
  r = requests.post(API_ENDPOINT + '/selections/', headers={'API_AUTH': api_auth}, data=selection)
  if not (200 <= r.status_code < 300):
    raise RuntimeError(r.content)
  r.close()

  selection = {
    'light_pattern_id': animations[animation_name]['id'],
    'light_pattern_name': animation_name
  }
  r = requests.post(API_ENDPOINT + '/selections/updatepi/', headers={'API_AUTH': api_auth}, data=selection)
  if not (200 <= r.status_code < 300):
    raise RuntimeError(r.content)
  r.close()

def preview_generated_animation(animation_id, api_auth):
  selection = {
    'id': animation_id
  }

  with requests.post(API_ENDPOINT + '/generate/preview/', headers={'API_AUTH': api_auth}, data=selection) as r:
    if not (200 <= r.status_code < 300):
      raise RuntimeError(r.content)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(prog="backend-cli", 
                                   description="A command line interface to our christmas lights backend for programatically controlling the lights, or for those who can't view the frontend.")
  parser.add_argument('--auth',
                      help='the authorization key for the backend api',
                      type=str,
                      required=True)
  parser.add_argument('-o', '--off',
                      help='turns off the lights',
                      action='store_true')
  parser.add_argument('-r', '--random',
                      help='selects a random animation',
                      action='store_true')
  parser.add_argument('-l', '--list',
                      help='lists all available animations',
                      action='store_true')
  parser.add_argument('-a', '--animation_name',
                      help='selects a specified animation',
                      type=str)
  parser.add_argument('-p', '--preview',
                      help='previews a specified generated animation',
                      type=str)

  args = parser.parse_args()

  animations = get_animations(args.auth)

  if args.list:
    print('\n'.join(['{}:\n\t{}'.format(animation['animation_id'], animation['description']) for animation in animations.values()]))
  elif args.off:
    turn_off_lights(animations, args.auth)
  elif args.random:
    turn_on_random(animations, args.auth)
  elif args.animation_name:
    turn_on_animation(animations, args.animation_name, args.auth)
  elif args.preview:
    preview_generated_animation(args.preview, args.auth)