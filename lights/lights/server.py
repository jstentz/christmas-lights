from flask import Flask, request
import pathlib
from typing import Any, Optional
from threading import Semaphore
from lights.run_animation import ThreadedAnimationRunner

BASE_PATH = pathlib.Path(__file__).parent
RUN_ANIMATION_PATH = BASE_PATH / 'run_animation.py'

ar: Optional[ThreadedAnimationRunner] = None
s = Semaphore()

app = Flask(__name__)

@app.route('/', methods=['POST'])
def receive_data():
  global ar
  data = request.get_json()
  animation = data['light_pattern_name']
  parameters = data['parameters']
  s.acquire()
  if ar is not None:
    ar.stop()
    ar.join()
  ar = ThreadedAnimationRunner(animation, 'SerialController', parameters)
  s.release()
  return 'Success!'

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8000)