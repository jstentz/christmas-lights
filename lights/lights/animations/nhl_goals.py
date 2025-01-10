import requests
import time
import numpy as np
from typing import Optional, Collection
from lights.animations.base import BaseAnimation
from lights.animations.goal_light import GoalLight
from lights.utils.geometry import POINTS_3D
import threading

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

class NHLGoals(BaseAnimation):
  def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = 60, speed : float = 0.02,
               rotation_speed : float = 0.01, bandwidth : float = 0.4):
    super().__init__(frameBuf, fps)

    # start as black and white
    self.colors = ColorWrapper(np.array([(255, 255, 255), (0, 0, 0)]))

    # start listening for nhl goals
    self.nhl_thread = threading.Thread(target=listen_for_goals, args=(self.colors,), daemon=True)
    self.nhl_thread.start()

    self.speed = speed
    self.rotation_speed = rotation_speed
    self.bandwidth = bandwidth

    self.goalLight = GoalLight(frameBuf)

    # center the points at the mid points
    min_pt = np.min(POINTS_3D, axis=0)
    max_pt = np.max(POINTS_3D, axis=0)
    mid_point = (max_pt + min_pt) / 2
    self.CENTERED_POINTS_3D = POINTS_3D - mid_point
    self.t = 0

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
    if self.colors.get_t() > 0:
      self.goalLight.renderNextFrame()
      self.goalLightT -= 1 / self.fps if self.fps is not None else 1 / 60
      return
    
    distances = np.dot(self.CENTERED_POINTS_3D, self.plane) + self.t
    colors = self.colors.get_colors()
    indices = ((distances // self.bandwidth) % len(colors)).astype(np.int32)
    colors = colors[indices]
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

class ColorWrapper:
  def __init__(self, colors: np.array) -> None:
    self.colors = colors
    self.t = 0
    self.lock = threading.Lock()

  def update_colors(self, new_colors: np.array):
    self.lock.acquire(blocking=True)
    self.colors = new_colors
    self.lock.release()

  def get_colors(self):
    self.lock.acquire(blocking=True)
    colors = self.colors
    self.lock.release()
    return colors
  
  def get_t(self):
    return self.t
  
  def set_t(self, t):
    self.t = t

BASE_API = 'https://api-web.nhle.com/v1'

def get_games_today() -> dict:
  response = requests.get(f'{BASE_API}/schedule/now')
  response = response.json()
  games = response['gameWeek'][0]['games']
  return games

def get_play_by_play(game: dict) -> dict:
  response = requests.get(f'{BASE_API}/gamecenter/{game["id"]}/play-by-play')
  response = response.json()
  return response

def get_goals(game: dict) -> dict:
  play_by_play: dict = get_play_by_play(game)
  plays = play_by_play['plays']
  goals = {play['eventId']: play for play in plays if play['typeDescKey'] == 'goal'}
  return goals

def get_goals_per_game(games: list[dict]) -> dict:
  return {game['id']: (game, get_goals(game)) for game in games}

def listen_for_goals(colors: ColorWrapper):
  games = get_games_today()
  known_goals_per_game = get_goals_per_game(games)

  while True:
    curr_goals_per_game = get_goals_per_game(games)
    
    new_goals_per_game = []

    for id, (game, goals) in curr_goals_per_game.items():
      new_goals_per_game.extend([(goal, game) for goal_id, goal in goals.items() if goal_id not in known_goals_per_game[id][1]])
      
    if new_goals_per_game:
      goal, game = new_goals_per_game[0]
      scoring_team_id = goal['details']['eventOwnerTeamId']
      home_team, away_team = game['homeTeam'], game['awayTeam']
      scoring_team_common_name = home_team['commonName']['default'] if scoring_team_id == home_team['id'] else away_team['commonName']['default']
      scoring_team_colors = colors_per_team[scoring_team_common_name]
      colors.update_colors(np.array(scoring_team_colors))
      colors.set_t(3)

    known_goals_per_game = curr_goals_per_game
    time.sleep(1)

