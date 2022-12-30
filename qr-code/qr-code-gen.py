from qrcodegen import *
import serial

SCREEN_WIDTH = 64
SCREEN_HEIGHT = 48

PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600
MAX_MESSAGE_LENGTH = 10
BITMAP_SIZE = 384

def to_bitmap(qrcode: QrCode, width: int, height: int):
  qr_width, qr_height = qrcode.get_size(), qrcode.get_size()
  if qr_width > width or qr_height > height:
    raise ValueError("Output size must be greater than qr code size")
  bitmap = [[0 for _ in range(width)] for _ in range(height)]

  ox = (width // 2) - (qr_width // 2)
  oy = 0#(height // 2) - (qr_height // 2)
  for x in range(qr_width):
    for y in range(qr_height):
      value = qrcode.get_module(x, y)
      bitmap[oy + y][ox + x] = 1 if value else 0

  return bitmap

def to_byte_index(r, c):
  return (r // 8 * SCREEN_WIDTH) + c, r % 8

def bitmap_to_bytearray(bitmap: List):
  height, width = len(bitmap), len(bitmap[0])
  output = [0 for _ in range((height * width + 7) // 8)]

  for r in range(height):
    for c in range(width):
      idx, bit = to_byte_index(r, c)
      output[idx] |= bitmap[r][c] << bit

  return output

def pad_message(message):
  if len(message) > MAX_MESSAGE_LENGTH:
    raise ValueError("Message of length {} exceeds the maximum length ({}).".format(len(message), MAX_MESSAGE_LENGTH))
  
  remainder = MAX_MESSAGE_LENGTH - len(message)
  return (" " * (remainder // 2)) + message + (" " * ((remainder + 1) // 2))

def update_password_and_url(message: str, url: str):
  message = pad_message(message)
  qr = QrCode.encode_text(url, QrCode.Ecc.MEDIUM)
  bitmap_bytes = bytes(bitmap_to_bytearray(to_bitmap(qr, SCREEN_WIDTH, SCREEN_HEIGHT)))
  if len(bitmap_bytes) != BITMAP_SIZE:
    raise RuntimeError("Wrong bitmap size!")
  password_bytes = message.encode("ascii")
  message = password_bytes + bitmap_bytes
  if len(message) != MAX_MESSAGE_LENGTH + BITMAP_SIZE:
    raise RuntimeError("Wrong message size!")
  ser = serial.Serial(PORT, BAUD_RATE)
  ser.write(message)
  ser.close()

if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser(prog="qr-code updater", 
                                   description="Sends a new password and qr-code to a microcontroller for displaying")
  
  parser.add_argument('password', type=str)
  parser.add_argument('-u', '--url', type=str, default='https://lights.ryanstentz.com/')
  args = parser.parse_args()

  update_password_and_url(args.password, args.url)