def is_valid_rgb_color(color):
  if len(color) != 3:
    return False
  for c in color:
    if c < 0 or c > 255:
      return False
  return True