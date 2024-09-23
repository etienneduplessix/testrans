from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
import requests
import random
from mysite.tools import myprint
from django.conf import settings
import os

API_UID = os.getenv('42_API_UID')
API_SECRET = os.getenv('42_API_SECRET')

def home(request):
	return render(request, 'index.html')


def get_template(request, template_name):
	if request.method == 'GET':
		template_path = os.path.join(settings.BASE_DIR, 'mysite/templates', f'{template_name}')
		myprint("HERE: ")
		myprint(template_path)
		if os.path.exists(template_path):
			# old version to open templates
			""" with open(template_path, 'r') as file:
				return HttpResponse(file.read(), content_type='text/html') """
			return render(request, template_name)
		else:
			# print("template NOT found: ", template_path)
			raise Http404("Template not found")
	return HttpResponse(status=405)


def load_template(request, template_name):
	myprint("load template")
	return redirect('/?template='+template_name)

# probably not necessary , test & delete
# def load_template(request, template_name):
# 	if template_name.endswith('.js'):
# 		template_path = os.path.join(settings.BASE_DIR, 'mysite/static/js', f'{template_name}')
# 		if os.path.exists(template_path):
# 			with open(template_path, 'r') as file:
# 				return HttpResponse(file.read(), content_type='application/js')
# 		else:
# 			raise Http404("Template no bueno")

# 	return redirect('/?template='+template_name)


# def load_profile(request, username):
#     myprint("load profile template")
#     return render(request, username)


def view_404(request, exception=None):
	# make a redirect to homepage
	# you can use the name of url or just the plain link
	return redirect('/') # or redirect('name-of-index-url')


def logout(request):
	request.session.flush()
	return redirect('/')

def game_view(request):
	return render(request, 'game.html')

def logout(request):
	request.session.flush()
	return redirect('/')


def callback(request):
	code = request.GET.get('code')
	state = request.GET.get('state')

	token_url = "https://api.intra.42.fr/oauth/token"
	client_id = API_UID  # Replace with your actual client_id
	client_secret = API_SECRET # Replace with your actual client_secret
	redirect_uri = "http://127.0.0.1:8000/api/callback"  # Replace with your actual redirect URI

	data = {
		'grant_type': 'authorization_code',
		'client_id': client_id,
		'client_secret': client_secret,
		'code': code,
		'redirect_uri': redirect_uri
	}
	try:
		# Exchange authorization code for access token
		response = requests.post(token_url, data=data)
		response.raise_for_status()  # Raise exception for HTTP errors

		token_data = response.json()
		access_token = token_data.get('access_token')

		# Fetch user data using the access token
		user_url = "https://api.intra.42.fr/v2/me"
		headers = {'Authorization': f'Bearer {access_token}'}
		user_response = requests.get(user_url, headers=headers)
		user_response.raise_for_status()

		user_data = user_response.json()
		user_name = user_data['login']  # Assuming 'login' is the key for user's name

		# Optionally, you can store the access_token securely for future API requests

		# Render home.html with user data
		return render(request, 'index.html', {'user_name': user_name})

	except requests.exceptions.HTTPError as http_err:
		return HttpResponse(f"HTTP error occurred: {http_err}", status=response.status_code)

	except requests.exceptions.RequestException as req_err:
		return HttpResponse(f"Request error occurred: {req_err}")

	except ValueError as val_err:
		return HttpResponse(f"Value error occurred: {val_err}")

	except Exception as err:
		return HttpResponse(f"Error occurred: {err}")

	return HttpResponse("Unknown error occurred", status=500)
