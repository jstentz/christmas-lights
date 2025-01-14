import numpy as np
from lights.animations.base import BaseAnimation
from lights.animations.goal_light import GoalLight
from lights.utils.geometry import POINTS_3D
import vlc
import os
from lights.utils.nhl import NHLGoalMonitor
from typing import Optional

colors_per_team = {
  'Ducks': [(252, 76, 2), (185, 151, 91), (193, 198, 200), (0, 0, 0)],
  'Bruins': [(252, 181, 20), (17, 17, 17)],
  'Sabres': [(0, 48, 135), (255, 184, 28), (255, 255, 255)],
  'Flames': [(210, 0, 28), (250, 175, 25), (255, 255, 255)],
  'Hurricanes': [(206, 17, 38), (255, 255, 255), (164, 169, 173), (0, 0, 0)],
  'Blackhawks': [(207,10,44), (255,103,27), (0,131,62), (255,209,0), (209,138,0), (0,25,112), (0,0,0), (255,255,255)],
  'Avalanche': [(111, 38, 61), (35, 97, 146), (162, 170, 173), (0, 0, 0)],
  'Blue Jackets': [(0,38,84), (206,17,38), (164,169,173)],
  'Stars': [(0, 200, 71), (143, 143, 140), (17, 17, 17)],
  'Red Wings': [(206,17,38), (255,255,255)],
  'Oilers': [(4, 30, 66), (252, 76, 0)],
  'Panthers': [(4,30,66), (200,16,46), (185,151,91)],
  'Kings': [(17,17,17), (162,170,173), (255,255,255)],
  'Wild': [(175, 35, 36), (2, 73, 48), (237, 170, 0), (226, 214, 181)],
  'Canadiens': [(175, 30, 45), (25, 33, 104)],
  'Predators': [(255,184,28), (4,30,66), (255,255,255)],
  'Devils': [(206, 17, 38), (0, 0, 0), (255, 255, 255)],
  'Islanders': [(0,83,155), (244, 125, 48)],
  'Rangers': [(0,56,168), (206,17,38), (255,255,255)],
  'Senators': [(0, 0, 0), (240, 26, 50), (183, 146, 87), (255, 255, 255)],
  'Flyers': [(247, 73, 2), (0, 0, 0), (255, 255, 255)],
  'Penguins': [(0,0,0), (207,196,147), (252,181,20), (255,255,255)],
  'Blues': [(0, 47, 135), (252, 181, 20), (4, 30, 66), (255, 255, 255)],
  'Sharks': [(0, 109, 117), (234, 114, 0), (0, 0, 0)],
  'Kraken': [(0, 22, 40), (153, 217, 217), (53, 84, 100), (104, 162, 185), (233, 7, 43)],
  'Lightning': [(0, 40, 104), (255, 255, 255)],
  'Maple Leafs': [(0, 32, 91), (255, 255, 255)],
  'Utah Hockey Club': [(113, 175, 229), (9, 9, 9), (255, 255, 255)],
  'Canucks': [(0, 32, 91), (10, 134, 61), (4, 28, 44), (153, 153, 154), (255, 255, 255)],
  'Golden Knights': [(185,151,91), (51,63,72), (200,16,46), (35,31,32), (255,255,255)],
  'Capitals': [(4, 30, 66), (200, 16, 46), (255,255,255)],
  'Jets': [(4,30,66), (0,76,151), (172,22,44), (123,48,62), (85,86,90), (142,144,144), (255,255,255)],
}

songs_per_team = {
  'Ducks': 'audio/ducks.mp3',
  'Bruins': 'audio/bruins.mp3',
  'Sabres': 'audio/sabres.mp3',
  'Flames': 'audio/flames.mp3',
  'Hurricanes': 'audio/hurricanes.mp3',
  'Blackhawks': 'audio/blackhawks.mp3',
  'Avalanche': 'audio/avalanche.mp3',
  'Blue Jackets': 'audio/blue_jackets.mp3',
  'Stars': 'audio/stars.mp3',
  'Red Wings': 'audio/red_wings.mp3',
  'Oilers': 'audio/oilers.mp3',
  'Panthers': 'audio/panthers.mp3',
  'Kings': 'audio/kings.mp3',
  'Wild': 'audio/wild.mp3',
  'Canadiens': 'audio/canadiens.mp3',
  'Predators': 'audio/predators.mp3',
  'Devils': 'audio/devils.mp3',
  'Islanders': 'audio/islanders.mp3',
  'Rangers': 'audio/rangers.mp3',
  'Senators': 'audio/senators.mp3',
  'Flyers': 'audio/flyers.mp3',
  'Penguins': 'audio/penguins.mp3',
  'Blues': 'audio/blues.mp3',
  'Sharks': 'audio/sharks.mp3',
  'Kraken': 'audio/kraken.mp3',
  'Lightning': 'audio/lightning.mp3',
  'Maple Leafs': 'audio/leafs.mp3',
  'Utah Hockey Club': 'audio/hockey_club.mp3',
  'Canucks': 'audio/canucks.mp3',
  'Golden Knights': 'audio/golden_knights.mp3',
  'Capitals': 'audio/capitals.mp3',
  'Jets': 'audio/jets.mp3',
}

path = os.path.dirname(os.path.abspath(__file__))

class NHLGoals(BaseAnimation):
  def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = 60, speed: float = 0.02,
               rotation_speed: float = 0.01, bandwidth: float = 0.4, 
               goal_light_duration: float = 7.0, play_horns: bool = True):
    super().__init__(frameBuf, fps)

    # start as black and white
    self.colors = np.array([(255, 255, 255), (0, 0, 0)])

    # start monitoring nhl goals
    self.goal_monitor = NHLGoalMonitor(1.0)
    self.goal_light = GoalLight(frameBuf)
    self.goal_light_duration = goal_light_duration
    self.goal_light_time_remaining = 0
    self.play_horns = play_horns
    self.vlc_instance = vlc.Instance()
    self.vlc_player = self.vlc_instance.media_player_new()
    self.goal_monitor.start()

    self.speed = speed
    self.rotation_speed = rotation_speed
    self.bandwidth = bandwidth
    self.t = 0

    # center the points at the mid points
    min_pt = np.min(POINTS_3D, axis=0)
    max_pt = np.max(POINTS_3D, axis=0)
    mid_point = (max_pt + min_pt) / 2
    self.CENTERED_POINTS_3D = POINTS_3D - mid_point

    # generate a random initial angle for the plane
    self.plane = NHLGoals.generateRandomPlane()
    self.target = NHLGoals.generateRandomPlane()
  
  # pick a random unit vector in 3D space
  @staticmethod
  def generateRandomPlane():
    while np.all((plane := np.random.normal(size=3)) == 0.0):
      pass
    return plane / np.linalg.norm(plane)

  def renderNextFrame(self):
    # step goal light animation if still in progress
    if self.goal_light_time_remaining > 0:
      self.goal_light.renderNextFrame()
      self.goal_light_time_remaining -= 1 / self.fps if self.fps is not None else 1 / 60
      return
    
    # check for new goals
    if scoring_team := self.goal_monitor.pop_goal():
      # update colors
      self.colors = np.array(colors_per_team[scoring_team])
      # start goal light animation on next render
      self.goal_light_time_remaining = self.goal_light_duration
      # play horn if enabled
      if self.play_horns:
        media = self.vlc_instance.media_new(os.path.join(path, songs_per_team[scoring_team]))
        self.vlc_player.set_media(media)
        self.vlc_player.play()

    distances = np.dot(self.CENTERED_POINTS_3D, self.plane) + self.t
    indices = ((distances // self.bandwidth) % len(self.colors)).astype(np.int32)
    colors = self.colors[indices]
    self.frameBuf[:] = colors

    # increment the time by the speed 
    self.t += self.speed

    # make progress towards the target plane
    diffs = self.target - self.plane
    self.plane += diffs * self.rotation_speed
    self.plane /= np.linalg.norm(self.plane)

    # move the target if we are close to it
    # TODO: make this related to rotation_speed so we don't overstep it 
    epsilon = 0.01
    if np.linalg.norm(self.plane - self.target) < epsilon:
      self.target = NHLGoals.generateRandomPlane()

  def shutdown(self):
    self.goal_monitor.stop()
