# cli.py
import requests

BASE_URL = 'http://127.0.0.1:8000/game_api/'

def get_game_state():
	response = requests.get(BASE_URL + 'state/')
	return response.json()

def move_paddle(paddle, direction):
	response = requests.post(BASE_URL + 'move/', json={'paddle': paddle, 'direction': direction})
	return response.json()

def update_game():
	response = requests.post(BASE_URL + 'update/')
	return response.json()

# Example usage
if __name__ == '__main__':
	print(get_game_state())
	move_paddle(1, 1)
	update_game()
	print(get_game_state())
