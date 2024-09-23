import requests
from urllib.parse import unquote

BASE_URL = 'http://127.0.0.1:8000/'
LOGIN_URL = BASE_URL + 'user_api/login/'
GAME_API_URL = BASE_URL + 'game_api/'
CSRF_URL = BASE_URL  # Example endpoint for CSRF token


def get_game_state(15):
    """Fetch game state after login."""
    response = session.get(GAME_API_URL + 'state/')
    return response.json()

def move_paddle(paddle, direction):
    """Move the paddle in the game."""
    response = session.post(GAME_API_URL + 'move/', json={'paddle': paddle, 'direction': direction})
    return response.json()

def update_game():
    """Update the game state."""
    response = session.post(GAME_API_URL + 'update/')
    return response.json()

