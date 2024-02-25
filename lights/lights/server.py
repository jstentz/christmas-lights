from flask import Flask, request
import pathlib
from typing import Optional
from threading import Semaphore
from lights.run_animation import ThreadedAnimationRunner
import json
import docker

BASE_PATH = pathlib.Path(__file__).parent
RUN_ANIMATION_PATH = BASE_PATH / 'run_animation.py'

ar: Optional[ThreadedAnimationRunner] = None
s = Semaphore()
d = docker.from_env()
container = None

app = Flask(__name__)
root_path = pathlib.Path(__file__).resolve().parent
generated_animation_path = root_path / 'animations/untrusted/ai.py'

@app.route('/preview', methods=['POST'])
def run_untrusted_animation():
  global container, ar
  data = request.get_json()
  animation_code = data['generated_animation']
  s.acquire()
  if ar is not None:
    ar.stop()
    ar.join()
    ar = None
  if container is not None:
    container.stop()
    container.wait()
    container = None
  with open(generated_animation_path, 'w') as f:
    f.write(animation_code)
  container = d.containers.run(
    'lights', 
    'python run_animation.py -c SerialController --file /mnt/animations/ai.py', 
    detach=True,
    network_mode='none',
    group_add=['65537'],
    devices=['/dev/ttyACM0:/dev/ttyACM0'],
    volumes={
      generated_animation_path.parent: {'bind': '/mnt/animations/', 'mode': 'ro'}
    }
  )
  s.release()
  return 'Success!'

@app.route('/', methods=['POST'])
def receive_data():
  global ar, container
  data = request.get_json()
  animation = data['light_pattern_name']
  parameters = data['parameters']
  s.acquire()
  if container is not None:
    container.stop()
    container.wait()
    container = None
  if ar is not None:
    ar.stop()
    ar.join()
    ar = None
  try:
    ar = ThreadedAnimationRunner.from_names(animation, 'SerialController', json.dumps(parameters))
    ar.start()
  except Exception as e:
    print(e)
  s.release()
  return 'Success!'

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8000)