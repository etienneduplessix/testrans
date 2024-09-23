from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .pong_game import *
from mysite.models import Game, GameUserRelation, User
import datetime
import threading
from django.shortcuts import get_object_or_404
from queue import Queue
from rest_framework.decorators import api_view
from rest_framework.response import Response
import datetime
import queue  
from mysite.tools import *
from django.utils.timezone import now

games = {}
game_queues = {}

class GameThread(threading.Thread):
    def __init__(self, game_id, game_instance, game_rel):
        super().__init__()
        self.game_id = game_id
        self.game_instance = game_instance
        self.game_rel = game_rel
        self.queue = queue.Queue()
        self.running = True

    def run(self):
        while self.running:
            self.game_instance.update()
            self.game_rel.score = self.game_instance.get_state()['score'][0]
            self.game_rel.save()

    def stop(self):
        self.running = False

    def get_state(self):
        return {
            'game_id': self.game_id,
            'running': self.running,
            'queue_size': self.queue.qsize()
        }


def run_game(game_obj, game_rel, game_instance):
    if game_obj is None:
        raise ValueError("game_obj cannot be None")
    game_thread = GameThread(game_obj.id, game_instance, game_rel)
    game_thread.start()
    games[game_obj.id] = game_instance
    game_queues[game_obj.id] = game_thread.queue
    return game_thread


@api_view(['POST'])
def start_game(request): 
    user_id = request.user.id
    game_user_relation = GameUserRelation.objects.filter(user_id=user_id).last()
    if not game_user_relation:
        return Response({"error": "GameUserRelation not found"}, status=status.HTTP_404_NOT_FOUND)
    
    game_id = game_user_relation.game_id
    print(game_id)
    game_obj = Game.objects.filter(id=game_id).first()
    if not game_obj:
        return Response({"error": "Game not found"}, status=status.HTTP_404_NOT_FOUND)
    
    game_tread = run_game(game_obj, game_user_relation, PongGame())
    print(game_tread)
    return Response({"message": "Game started"})


def create_or_get_recent_game():
    """Helper function to create a game or get the most recent game if within 2 seconds."""
    current_time = now()

    try:
        # Get the most recent game
        last_game = Game.objects.latest('date_time_start')

        # Check if the last game was created within the last 2 seconds
        time_difference = (current_time - last_game.date_time_start).total_seconds()
        if time_difference <= 2:
            return last_game
    except Game.DoesNotExist:
        # No games exist, so we need to create one
        pass

    # Create a new game if no recent game was found within 2 seconds
    game_obj = Game(
        date_time_start=current_time,
        date_time_end=current_time,  # End time is set to start time initially
    )
    game_obj.save()
    return game_obj

@api_view(['POST'])
def find_adv(request):
    user = request.user
    game_rel = GameUserRelation.objects.filter(user=user).first()

    return Response({"game_id": game_obj.id})
@api_view(['POST'])
def initialize_game(request):
    user = request.user
    game_obj = create_or_get_recent_game()
    # Check if a GameUserRelation already exists for this game and user
    if not GameUserRelation.objects.filter(game=game_obj, user=user).exists():
        # Create a GameUserRelation for the initiating user
        game_rel = GameUserRelation(
            game=game_obj,
            user=user,
            score=0,
        )
        game_rel.save()

    return Response({"game_id": game_obj.id})

@api_view(['POST'])
def intirelation(request):
    game_obj = create_or_get_recent_game()
    # Ensure a relation for the current user is only created once
    if not GameUserRelation.objects.filter(game=game_obj, user=request.user).exists():
        game_rel1 = GameUserRelation(
            game=game_obj,
            user=request.user,
            score=0,
        )
        game_rel1.save()

    # Ensure a relation for the second user is only created once
    second_user = User.objects.get(username=request.data.get('to'))
    if not GameUserRelation.objects.filter(game=game_obj, user=second_user).exists():
        game_rel2 = GameUserRelation(
            game=game_obj,
            user=second_user,
            score=0,
        )
        game_rel2.save()

    return Response({"game_id": game_obj.id, "user1_id": request.user.id, "user2_id": second_user.id})



@api_view(['POST'])
def stop_game(request):
    game_id = request.session.get('game_id')
    if game_id not in games:
        return Response({"error": "Game not found"}, status=404)

    game_thread = game_queues[game_id]
    game_thread.stop()

    state = games[game_id].get_state()

    if state['score'][0] == 5 or state['score'][1] == 5:
        try:
            game_obj = Game.objects.get(id=game_id)
            game_obj.date_time_end = datetime.datetime.now()
            game_obj.save()
        except Game.DoesNotExist:
            return Response({'error': 'Game not found'}, status=404)

    return Response(state)

@api_view(['POST'])
def delete_game(request):
    game_id = request.session.get('game_id')
    if game_id not in games:
        return Response({"error": "Game not found"}, status=404)

    game_thread = game_queues[game_id]
    game_thread.stop()

    del games[game_id]
    del game_queues[game_id]

    return Response({"message": "Game deleted"})

@api_view(['POST'])
def update_game(request):
    user_id = request.user.id
    print(user_id)
    game_user_relation = GameUserRelation.objects.filter(user_id=user_id).first()
    if not game_user_relation:
        return Response({"error": "GameUserRelation not found"}, status=status.HTTP_404_NOT_FOUND)
    game_id = game_user_relation.game_id
    myprint(game_id)
    def task():
        game = games[game_id]
        game.update()
        game_state = game.get_state()
        game_rel = get_object_or_404(GameUserRelation, user=request.user, game_id=game_id)
        game_rel.score = game_state['score'][0]
        game_rel.save()

    game_queues[game_id].put(task)
    return Response(games[game_id].get_state())

@api_view(['POST'])
def move_paddle(request):
    user_id = request.user.id
    game_user_relation = GameUserRelation.objects.filter(user_id=user_id).last()
    game_id = game_user_relation.game_id 
    def task():
        games[game_id].move_paddle(paddle, direction)
        print(paddle, direction)

    game_queues[game_id].put(task)
    return Response(games[game_id].get_state())

@api_view(['GET'])
def get_game_state(request, game_id):
    game_thread = games.get(game_id)
    if game_thread is None:
        return Response({"error": "Game not found"}, status=404)

    state = game_thread.get_state()
    print(state)
    return Response(state)
