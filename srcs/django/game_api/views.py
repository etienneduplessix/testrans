from mysite.models import User
from mysite.tools import myprint

from django.http import JsonResponse
from django.core import serializers

import json

# from .serializer import UserSerializer

def who_am_i(request):
	myprint (request.method + " REQUEST TO WHOAMI")
	myprint (request.session)

	if 'login' not in request.session:
		return JsonResponse({'error': 'no:('})

	# # this gives you a list of dicts
	# raw_data = serializers.serialize('json', User.objects.filter(username=request.session['login']))
	# # now extract the inner `fields` dicts
	# actual_data = [d['fields'] for d in raw_data]
	# # and now dump to JSON
	# output = json.dumps(actual_data)


	data = User.objects.filter(username=request.session['login'])
	# data = User.objects.all()
	output = serializers.serialize("json", data)

	myprint(output)

	return JsonResponse(output, safe=False)