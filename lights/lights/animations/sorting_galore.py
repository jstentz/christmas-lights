import numpy as np
from lib.base_animation import BaseAnimation
from utils.geometry import POINTS_3D
from utils.colors import hsv_to_rgb

# Mescad's Sorting Algorithm Visualizer
#
# This animation generates an initial random color for each light on the tree, 
# and then sorts the colors using various sorting algorithms. Light colors are
# updated during the sort so that we can see how the various sorting strategies work.
# 
# For each algorithmn, the lights are sorted, and then "unsorted" back to their original
# color states using the same algorithmn. The animation automatically uses all included
# sorting algorithms with the same initial color data, and then generates a new set of colors 
# before starting over with the first algorithm.


# The Sorting Algorithms
# Six algorithmns are included. 
# They are Shell Sort, Cocktail Shaker Sort, Radix Sort, Gnome Sort, Bubble Sort, and Counting Sort. 
# These were chosen for their visual differences. 
# 
# Each algorithm is independent, so you can easily drop in new ones to see how they look on the tree.

# Shell Sort, a fast sorting algorithm
def shell_sort(color_values, original_indices, mode):
  n = len(color_values)
  gap = n // 2
  while gap:
    for i in range(gap, n):
      cv, oi = color_values[i], original_indices[i]
      j = i
      while j >= gap and (
        (original_indices[j - gap] if mode == "unsort" else color_values[j - gap]) >
        (oi if mode == "unsort" else cv)
      ):
        color_values[j] = color_values[j - gap]
        original_indices[j] = original_indices[j - gap]
        j -= gap
        yield
      color_values[j] = cv
      original_indices[j] = oi
      yield
    gap //= 2

# Bubble Sort, a slow sorting algorithm that is visually pleasing
def bubble_sort(color_values, original_indices, mode):
  n = len(color_values)
  for end in range(n - 1, 0, -1):
    for i in range(end):
      a = original_indices[i] if mode == "unsort" else color_values[i]
      b = original_indices[i + 1] if mode == "unsort" else color_values[i + 1]
      if a > b:
        color_values[i], color_values[i + 1] = color_values[i + 1], color_values[i]
        original_indices[i], original_indices[i + 1] = (
          original_indices[i + 1], original_indices[i]
        )
      yield

# Counting Sort, a fast sorting algorithm. This one was too fast, so we run it in a special slow mode
def counting_sort(color_values, original_indices, mode):
  n = len(color_values)
  m = n if mode == "unsort" else 256
  src = original_indices if mode == "unsort" else color_values

  counts = [0] * m
  for x in src:
    counts[int(x)] += 1
    yield

  total = 0
  for i in range(m):
    counts[i], total = total, total + counts[i]
    yield

  out_colors = [0] * n
  out_indices = [0] * n
  for i in range(n):
    k = int(original_indices[i] if mode == "unsort" else color_values[i])
    p = counts[k]
    out_colors[p] = int(color_values[i])
    out_indices[p] = int(original_indices[i])
    counts[k] += 1
    yield

  for i in range(n):
    color_values[i] = out_colors[i]
    original_indices[i] = out_indices[i]
    yield

# Radix Sort, a very fast sorting algorithm 
def radix_sort(color_values, original_indices, mode):
  n = len(color_values)
  src = original_indices if mode == "unsort" else color_values
  max_val = n - 1 if mode == "unsort" else 255

  exp = 1
  while max_val // exp > 0:
    count = [0] * 10

    # count digits
    for i in range(n):
      digit = (src[i] // exp) % 10
      count[digit] += 1
      yield

    # prefix sum
    total = 0
    for i in range(10):
      count[i], total = total, total + count[i]
      yield

    out_colors = [0] * n
    out_indices = [0] * n

    # stable placement
    for i in range(n):
      digit = (src[i] // exp) % 10
      pos = count[digit]
      out_colors[pos] = color_values[i]
      out_indices[pos] = original_indices[i]
      count[digit] += 1
      yield

    # copy back
    for i in range(n):
      color_values[i] = out_colors[i]
      original_indices[i] = out_indices[i]
      yield

    exp *= 10

# Gnome Sort, a visually interesting sorting algorithm (my favorite)
def gnome_sort(color_values, original_indices, mode):
  n = len(color_values)
  i = 1

  while i < n:
    left = original_indices[i - 1] if mode == "unsort" else color_values[i - 1]
    right = original_indices[i] if mode == "unsort" else color_values[i]

    if left <= right:
      i += 1
    else:
      # swap
      color_values[i], color_values[i - 1] = color_values[i - 1], color_values[i]
      original_indices[i], original_indices[i - 1] = (
        original_indices[i - 1], original_indices[i]
      )
      i = max(1, i - 1)

    yield
    
# Cocktail Shaker Sort, like a faster Bubble Sort that works from the ends toward the middle
def cocktail_shaker_sort(color_values, original_indices, mode):
  n = len(color_values)
  start = 0
  end = n - 1
  swapped = True
  tick = 0

  def key(i):
    return original_indices[i] if mode == "unsort" else color_values[i]

  while swapped:
    swapped = False

    # forward pass
    for i in range(start, end):
      tick += 1
      if key(i) > key(i + 1):
        color_values[i], color_values[i + 1] = color_values[i + 1], color_values[i]
        original_indices[i], original_indices[i + 1] = original_indices[i + 1], original_indices[i]
        swapped = True
        yield  # yield on swap = smoother
      elif (tick & 63) == 0:
        yield  # occasional yield so it animates even without swaps

    if not swapped:
      break

    swapped = False
    end -= 1

    # backward pass
    for i in range(end, start, -1):
      tick += 1
      if key(i - 1) > key(i):
        color_values[i - 1], color_values[i] = color_values[i], color_values[i - 1]
        original_indices[i - 1], original_indices[i] = original_indices[i], original_indices[i - 1]
        swapped = True
        yield
      elif (tick & 63) == 0:
        yield

    start += 1


# The animation steps through each algorithm, 
#  pausing for 3 seconds between to allow time 
# to admire the final state.

class SortingGalore(BaseAnimation):
  def __init__(self, frameBuf, *, fps=15, hold_seconds=3, hue_end=0.75, seed=None,):
    super().__init__(frameBuf, fps=fps)

    self.n = len(frameBuf)
    self.hold = 45 #3 second pause between each sort at 15 fps
    self.rng = np.random.default_rng(seed)

    pts = np.asarray(POINTS_3D)
    order = np.argsort(pts[:, 2])[::-1]  # fixed contest geometry: Z axis, top=max
    self.pixel_from_sorted = np.empty(self.n, dtype=np.int32)
    self.pixel_from_sorted[order] = np.arange(self.n, dtype=np.int32)

    self.color_values = np.zeros(self.n, dtype=np.uint8)
    self.original_indices = np.zeros(self.n, dtype=np.int32)

    h = float(np.clip(hue_end, 0.0, 0.95))
    self.lut = np.zeros((256, 3), dtype=np.uint8)
    for i in range(256):
      self.lut[i] = hsv_to_rgb(h * (i / 255.0), 1.0, 1.0)

    self._g = self.main()

  def draw(self):
    self.frameBuf[:] = self.lut[self.color_values[self.pixel_from_sorted]]

  # This is used to pause briefly, so we can see the finished state before moving on
  def hold_draw(self):
    for _ in range(self.hold):
      self.draw()
      yield


  #The sorts are run as a generator function so that we can see the intermediate
  #sorting steps along the way
  def run_sort(self, sorting_algorithm, mode, steps_per_frame):
    gen = sorting_algorithm(self.color_values, self.original_indices, mode)
    while True:
      for _ in range(steps_per_frame):
        try:
          next(gen)
        except StopIteration:
          self.draw()
          yield
          return
      self.draw()
      yield

  def main(self):
    
    #How many sorting steps are executed per animation frame
    FAST = 300 #Most algorithms use this, 300 steps per frame
    SLOW = 10  #Counting Sort is too fast, so we run it slower so we can see it working

    while True:

      #generate a set of new colors. 
      # We store integers for easy sorting and later map these values to HSV colors for display
      original_colors = self.rng.integers(0, 256, size=self.n, dtype=np.uint8)
      
      #store the initial color locations via index. We use this to "unsort" later
      original_indices = np.arange(self.n, dtype=np.int32)

      self.color_values[:] = original_colors
      self.original_indices[:] = original_indices
      yield from self.hold_draw()

      # Loop through each sorting algorithm
      # To add a new sorting algorithm, define it as a function above and add it to this list of algorithms.
      # To remove one from the animation, just remove it from this list.
      for sorting_algorithm in (shell_sort, cocktail_shaker_sort, radix_sort, gnome_sort, bubble_sort, counting_sort):
        self.color_values[:] = original_colors
        self.original_indices[:] = original_indices

        #Run them all fast, except for Counting Sort because it was instant
        steps_per_frame = SLOW if sorting_algorithm is counting_sort else FAST 

        #For each algorithm, we want to see it sort the random colors into a pattern
        #and then "unsort" it back to the original random state we started with.
        #This allows us to compare the performance of each algorithm on the same data
        for mode in ("sort", "unsort"):
          yield from self.run_sort(sorting_algorithm, mode, steps_per_frame)
          yield from self.hold_draw() # pause to admire the work 

  def renderNextFrame(self):
    try:
      next(self._g)
    except StopIteration:
      self._g = self.main()
      next(self._g)
