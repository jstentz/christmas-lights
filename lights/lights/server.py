from flask import Flask, request
from subprocess import Popen
import pathlib
from typing import Optional

ID_TO_FILENAME = {
  0: 'redlights.py',
  1: 'greenlights.py',
  2: 'snake.py',
  3: 'snowflakes.py',
  4: 'rainbow.py'
}

BASE_PATH = pathlib.Path(__file__).parent
ANIMATIONS_PATH = BASE_PATH / 'animations'

p: Optional[Popen[bytes]] = None

app = Flask(__name__)

@app.route('/', methods=['POST'])
def receive_data():
  data = request.get_json()
  print(data)
  return 'Success!'

@app.route('/select', methods=['GET'])
def handle_select():
  global p
  if p is not None:
    p.terminate()
  p = Popen(['python', ANIMATIONS_PATH/'dummy.py'])
  return 'Success!'

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8000)