import threading
import requests
from collections import deque

BASE_API = 'https://api-web.nhle.com/v1'

class NHLGoalMonitor():
  def __init__(self, pollingRate: float):
    # Thread-safe: only accessed by the worker thread.
    self.games = []
    self.known_goals_per_game = []
    self.polling_rate = pollingRate
    # Not thread-safe: accessed by both the worker thread and main thread.
    self.goals_queue = deque()
    self.queue_lock = threading.Lock()

    self.shutdown_event = threading.Event()
    self.worker_thread = threading.Thread(target=self.listen_for_goals, daemon=True)

  def start(self):
    self.worker_thread.start()

  def stop(self):
    self.shutdown_event.set()
    self.worker_thread.join()

  def pop_goal(self):
    with self.queue_lock:
      if self.goals_queue:
        return self.goals_queue.pop()
      return None

  def push_goal(self, scoringTeamName: str):
    with self.queue_lock:
      self.goals_queue.append(scoringTeamName)

  def listen_for_goals(self):
    games = get_games_today()
    known_goals_per_game = get_goals_per_game(games)

    while not self.shutdown_event.is_set():
      curr_goals_per_game = get_goals_per_game(games)
      
      new_goals_per_game = []

      for id, (game, goals) in curr_goals_per_game.items():
        new_goals_per_game.extend([(goal, game) for goal_id, goal in goals.items() if goal_id not in known_goals_per_game[id][1]])
        
      if new_goals_per_game:
        goal, game = new_goals_per_game[0]
        scoring_team_id = goal['details']['eventOwnerTeamId']
        home_team, away_team = game['homeTeam'], game['awayTeam']
        scoring_team_common_name = home_team['commonName']['default'] if scoring_team_id == home_team['id'] else away_team['commonName']['default']
        self.push_goal(scoring_team_common_name)

      known_goals_per_game = curr_goals_per_game
      self.shutdown_event.wait(self.polling_rate)


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