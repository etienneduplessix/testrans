# from django.shortcuts import redirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, authenticate
from mysite.tools import myprint
from rest_framework.decorators import api_view
from django.http import JsonResponse#, HttpResponse, HttpResponseBadRequest
from django.core import serializers
from mysite.models import User, Game, GameUserRelation, Friend, FriendshipRequest
import json
import datetime
from django.db.models import Max, Q
# from datetime import datetime
from django.utils import timezone

@api_view(['POST',])
def register_view(request):
	myprint("from register_view")
	if request.method == 'POST':
		try:
			data = request.POST
			user = User(
				username=data.get('username'),
				email=data.get('email'),
				intra_oauth=False,
				image_link="https://cdn.intra.42.fr/users/1a564b880ba6b36e5b509923753d7a9a/marvin.jpg"
			)
			user.set_password(data.get('password')),
			myprint("password: " + str(data.get('password')))
			myprint("password_hash: " + str(user.password))
			user.save()
			login(request, user)
			request.session['login'] = user.username
			request.session['user_id'] = user.id
			return JsonResponse({'status': 200, 'message': 'user added!'})
		except Exception as e:
			return JsonResponse({'status': 400, 'message': str(e)})


@api_view(['PUT'])
def profile(request, id):
	myprint (request.method + " REQUEST TO PROFILE")
	if request.user.id != id:
		return JsonResponse({'status': 403, 'message': 'Permission denied'})
	try:
		data = request.POST
		user = User.objects.get(id=id)
		if data.get('username') and data.get('username') != user.username:
			user.username = data.get('username')
		if data.get('email') and data.get('email') != user.email:
			user.email = data.get('email')
		if data.get('first_name') and data.get('first_name') != user.first_name:
			user.username = data.get('first_name')
		if data.get('last_name') and data.get('last_name') != user.last_name:
			user.email = data.get('last_name')
		user.save()
		request.session['login'] = user.username
		return JsonResponse({'status': 200, 'message': 'user information updated'})
	except Exception as e:
		return JsonResponse({'status': 400, 'message': str(e)})


@api_view(['PUT'])
def change_pass(request, id):
	myprint (request.method + " REQUEST TO CHANGE PASS")
	if request.user.id != id:
		return JsonResponse({'status': 403, 'message': 'Permission denied'})
	try:
		data = request.POST
		user = User.objects.get(id=id)
		if not check_password(data.get('old_password'), user.password):
			return JsonResponse({'status': 400, 'message': 'Password is incorrect'})
		new_password = data.get('new_password')
		if new_password != data.get('password_confirm'):
			return JsonResponse({'status': 400, 'message': 'Passwords do not match'})
		user.set_password(new_password)
		user.save()
		login(request, user)
		request.session['login'] = user.username
		request.session['user_id'] = user.id
		return JsonResponse({'status': 200, 'message': 'User password changed'})
	except Exception as e:
		return JsonResponse({'status': 400, 'message': str(e)})


@api_view(['GET'])
def get_profile_data(request):
	myprint (request.method + " REQUEST TO GET PROFILE DATA")
	if request.user.is_authenticated:
		user = request.user

		# Retrieve all games the user participated in
		game_relations = GameUserRelation.objects.filter(user=user)
		total_games = game_relations.count()
		# To calculate total wins, find games where the user's score is the maximum among all participants
		total_wins = 0
		for relation in game_relations:
			# Check if the user's score is the highest in this game
			max_score = GameUserRelation.objects.filter(game=relation.game).aggregate(Max('score'))['score__max']
			if relation.score == max_score:
				total_wins += 1
		# Calculate total losses as games the user participated in but did not win
		total_losses = total_games - total_wins

		# Prepare match history
		match_history = []
		for relation in game_relations.select_related('game'):
			# Get all users who played in the same game
			opponents = GameUserRelation.objects.filter(game=relation.game).exclude(user=user)

			# Create a list of opponent usernames
			opponent_usernames = [opponent.user.username for opponent in opponents]

			# Calculate the match duration
			duration = relation.game.date_time_end - relation.game.date_time_start
			duration_seconds = duration.total_seconds()
			match_duration = f"{int(duration_seconds // 60)}:{int(duration_seconds % 60):02d}"  # Format as mm:ss

			match_info = {
				'date_time_start': relation.game.date_time_start.strftime('%Y-%m-%d %H:%M:%S'),
				'opponents': opponent_usernames,  # This includes all opponent usernames
				'match_duration': match_duration,
				'score': relation.score,
			}
			myprint(match_info)
			match_history.append(match_info)

		# Prepare the data to be sent as JSON
		data = {
			'username': user.username,
			'email': user.email,
			'first_name': user.first_name,
			'last_name': user.last_name,
			'avatar_url': user.image_link,
			'id': user.id,
			# 'avatar_url': user.profile.avatar.url if user.profile.avatar else '',

			# Game statistics
			'total_games': total_games,
			'total_wins': total_wins,
			'total_losses': total_losses,

			# Match history
			'match_history': match_history,
		}

		return JsonResponse({'status': 200, 'data': data})
	else:
		return JsonResponse({'status': 403, 'message': 'User not authenticated'})


@api_view(['GET'])
def get_friends(request):
	myprint (request.method + " REQUEST TO FRIENDS")
	if request.user.is_authenticated:
		user = request.user
		# Retrieve all friends for the user
		friendships = Friend.objects.filter(Q(user1=user) | Q(user2=user))
		# Prepare the list of friends' data
		friends_data = []
		for friendship in friendships:
			# Determine the friend based on the user
			friend = friendship.user2 if friendship.user1 == user else friendship.user1
			friends_data.append({
				'username': friend.username,
				'first_name': friend.first_name,
				'last_name': friend.last_name,
				'avatar_url': friend.image_link,  # Adjust according to your User model
			})

		# Prepare the data to be sent as JSON
		data = {
			'friends': friends_data,  # Include friends data
		}
		return JsonResponse({'status': 200, 'data': data})
	else:
		return JsonResponse({'status': 403, 'message': 'User not authenticated'})


@api_view(['GET'])
def who_am_i(request):
	myprint (request.method + " REQUEST TO WHOAMI")
	if request.user.is_anonymous:
		return JsonResponse({'status': 401, 'error': 'You are not logged in'})
	# if 'login' not in request.session:
	#     return JsonResponse({'status': 401, 'error': 'you are not logged in'})
	# print(request.session['login'])
	data = User.objects.filter(username=request.session['login'])
	serialized_data = serializers.serialize("json", data, fields=('username', 'first_name', 'last_name', 'email', 'image_link', 'last_seen'))
	# Deserialize the serialized data to a list of dictionaries
	deserialized_data = json.loads(serialized_data)
	for obj in deserialized_data:
		obj['fields']['id'] = obj['pk']
	actual_data = [d['fields'] for d in deserialized_data]
	# Add the status field
	response_data = {
		'status': 200,
		'data': actual_data
	}
	# Serialize the updated data to JSON
	output = json.dumps(response_data)
	return JsonResponse(output, safe=False)


@api_view(['GET'])
def who_is(request, username):
	myprint (request.method + " REQUEST TO WHOIS")
	if request.user.is_anonymous:
		return JsonResponse({'status': 401, 'error': 'You are not logged in'})
	# if 'login' not in request.session:
	#     return JsonResponse({'status': 401, 'error': 'you are not logged in'})

	data = User.objects.filter(username=username)
	if not data.exists:
		return JsonResponse({'status': 404, 'error': 'user does not exist'})
	serialized_data = serializers.serialize("json", data)
	# Deserialize the serialized data to a list of dictionaries. get only the
	deserialized_data = json.loads(serialized_data)[0]
	# Add the status field
	response_data = {
		'status': 200,
		'data': deserialized_data['fields']
	}
	# Serialize the updated data to JSON
	output = json.dumps(response_data)
	return JsonResponse(output, safe=False)


@api_view(['GET'])
def online(request):
	myprint (request.method + " REQUEST TO ONLINE")
	if request.user.is_anonymous:
		return JsonResponse({'status': 401, 'error': 'You are not logged in'})
	# if 'login' not in request.session:
	#     return JsonResponse({'status': 401, 'error': 'user not logged in'})
	five_minutes_ago = datetime.now() - datetime.timedelta(minutes=5)
	data = User.objects.filter(last_seen__lte=five_minutes_ago)
	output = serializers.serialize("json", data)
	return JsonResponse(output, safe=False)


@api_view(['POST'])
def login_view(request):
	myprint("from login view")
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			request.session['login'] = username
			request.session['user_id'] = user.id
			myprint("successful login")
			print(request.user)
			return JsonResponse({'status': 200, 'message': 'you are logged in'})
		else:
			return JsonResponse({'status': 400, 'message': 'Invalid credentials'})
	return JsonResponse({'status': 400, 'message': 'Invalid request method'})




