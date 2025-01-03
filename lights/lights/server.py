from flask import Flask, request
import pathlib
from typing import Optional
from threading import Semaphore
from lights.run_animation import ThreadedAnimationRunner
import json
import docker
import signal

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
  parameters = json.dumps(data['parameters_json'])
  s.acquire()
  if ar is not None:
    ar.stop()
    ar.join()
    ar = None
  if container is not None:
    container.stop()
    container.wait()
    container.remove()
    container = None
  with open(generated_animation_path, 'w') as f:
    f.write(animation_code)
  container = d.containers.run(
    'lights', 
    f'python run_animation.py -c SerialController --file /mnt/animations/ai.py --args \'{parameters}\' --no_validation', 
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
    container.remove()
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

def _shutdown():
  if ar is not None:
    ar.stop()
    ar.join()
  if container is not None:
    container.stop()
    container.wait()
    container.remove()

def _handle_sigterm(*args):
  _shutdown()
  exit(0)

def _handle_sigint(*args):
  _shutdown()
  exit(0)

if __name__ == '__main__':
  signal.signal(signal.SIGTERM, _handle_sigterm)
  signal.signal(signal.SIGINT, _handle_sigint)
  app.run(host="0.0.0.0", port=8000)