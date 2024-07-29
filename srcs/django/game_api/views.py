
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from mysite.models import User
from django.shortcuts import redirect
import json

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .pong_game import PongGame

game = PongGame()

@api_view(['GET'])
def get_game_state(request):
	return Response(game.get_state())

@api_view(['POST'])
def move_paddle(request):
	paddle = request.data.get('paddle')
	direction = request.data.get('direction')
	game.move_paddle(paddle, direction)
	return Response(game.get_state())

@api_view(['POST'])
def update_game(request):
	game.update()
	return Response(game.get_state())

