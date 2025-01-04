import requests
import time

BASE_API = 'https://api-web.nhle.com/v1'

def get_games_today() -> dict:
  response = requests.get(f'{BASE_API}/schedule/now')
  response = response.json()
  games = response['gameWeek'][0]['games']
  return games

def get_play_by_play(game: dict) -> dict:
  response = requests.get(f'{BASE_API}/gamecenter/{game['id']}/play-by-play')
  response = response.json()
  return response

def get_goals(game: dict) -> dict:
  play_by_play: dict = get_play_by_play(game)
  plays = play_by_play['plays']
  goals = {play['eventId']: play for play in plays if play['typeDescKey'] == 'goal'}
  return goals

def get_goals_per_game(games: list[dict]) -> dict:
  return {game['id']: (game, get_goals(game)) for game in games}


def listen_for_goals():
  games = get_games_today()
  known_goals_per_game = get_goals_per_game(games)

  while True:
    curr_goals_per_game = get_goals_per_game(games)
    
    new_goals_per_game = []

    for id, (game, goals) in curr_goals_per_game.items():
      new_goals_per_game.extend([(goal, game) for goal_id, goal in goals.items() if goal_id not in known_goals_per_game[id][1]])
      
    if new_goals_per_game:
      print(new_goals_per_game)

    known_goals_per_game = curr_goals_per_game
    time.sleep(1)


if __name__ == "__main__":
  # play_by_play: dict = get_play_by_play(game)

  # home_team = play_by_play['homeTeam']['commonName']['default']
  # away_team = play_by_play['awayTeam']['commonName']['default']

  listen_for_goals()