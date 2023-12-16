def is_valid_rgb_color(color):
  if len(color) != 3:
    return False
  for c in color:
    if c < 0 or c > 255:
      return False
  return True

def is_valid_inclusive_range(r, m, M):
  if len(r) != 2:
    return False
  if r[0] > r[1]:
    return False
  if (not (m <= r[0] <= M)) or (not (m <= r[1] <= M)):
    return False
  return True