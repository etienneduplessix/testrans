from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from mysite.models import User
from mysite.tools import myprint

from django.http import JsonResponse
from django.core import serializers
import datetime

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

import json


@api_view(['GET'])
def who_am_i(request):
	myprint (request.method + " REQUEST TO WHOAMI")

	if 'login' not in request.session:
		return JsonResponse({'status': -22})

	# # this gives you a list of dicts
	# raw_data = serializers.serialize('json', User.objects.filter(username=request.session['login']))
	# # now extract the inner `fields` dicts
	# actual_data = [d['fields'] for d in raw_data]
	# # and now dump to JSON
	# output = json.dumps(actual_data)


	data = User.objects.filter(username=request.session['login'])
	# data = User.objects.all()
	serialized_data = serializers.serialize("json", data)

	# Deserialize the serialized data to a list of dictionaries
	deserialized_data = json.loads(serialized_data)
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
def online(request):
	myprint (request.method + " REQUEST TO WHOAMI")

	if 'login' not in request.session:
		return JsonResponse({'status': -22, 'error' : 'user not logged in'})

	five_minutes_ago = datetime.now() - datetime.timedelta(minutes=5)

	data = User.objects.filter(last_seen__lte=five_minutes_ago)
	output = serializers.serialize("json", data)

	return JsonResponse(output, safe=False)


@api_view(['POST',])
def register(request):
	myprint("from register_view")
	if request.method == 'POST':
		try:
			data = request.POST
			user = User(
				username=data.get('username'),
				email=data.get('email'),
				intra_oauth=False,
				password_hash=make_password(data.get('password')),
				image_link="https://cdn.intra.42.fr/users/1a564b880ba6b36e5b509923753d7a9a/marvin.jpg"
			)
			user.save()
			request.session['login'] = data.get('username')
			return JsonResponse({'status': 200, 'message' : 'user added!'})
			# return redirect('/') #should be smtn inside HttpResponse instead of redirect
		except Exception as e:
			return JsonResponse({'status': 400, 'message' : str(e)})

@api_view(['POST',])
def login(request):
	myprint("from login view")
	data = request.POST
	login_username = data.get('username')
	login_password = data.get('password')

	if User.objects.filter(username=login_username).count() < 1:
		return JsonResponse({'status': 22, 'message' : 'user does not exist :('})

	myuser = User.objects.get(username=login_username)

	if not check_password(login_password, myuser.password_hash):
		return JsonResponse({'status': 22, 'message': 'password is incorrect :('})


	request.session['login'] = data.get('username')
	return JsonResponse({'status': 200, 'message' : 'user logged in!'})
	# return redirect('/') #should be smtn inside HttpResponse instead of redirect

