from flask import Flask, request
import subprocess
import pathlib
from typing import Optional
import sys
from threading import Semaphore

# ID_TO_FILENAME = {
#   0: 'redlights.py',
#   1: 'greenlights.py',
#   2: 'snake.py',
#   3: 'snowflakes.py',
#   4: 'rainbow.py'
# }

BASE_PATH = pathlib.Path(__file__).parent
RUN_ANIMATION_PATH = BASE_PATH / 'run_animation.py'

p: Optional[subprocess.Popen[bytes]] = None
s = Semaphore()

app = Flask(__name__)

@app.route('/', methods=['POST'])
def receive_data():
  global p
  data = request.get_json()
  animation = data['light_pattern_name']
  s.acquire()
  if p is not None:
    p.terminate()
    p.wait()
  p = subprocess.Popen([sys.executable, RUN_ANIMATION_PATH, '-r', '-a', animation])
  s.release()
  return 'Success!'

# @app.route('/select', methods=['GET'])
# def handle_select():
#   global p
#   if p is not None:
#     p.terminate()
#   p = Popen(['python', ANIMATIONS_PATH/'dummy.py'])
#   return 'Success!'

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8000)