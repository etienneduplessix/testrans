from django.shortcuts import redirect
from django.http import HttpResponse
import requests
import string, random
from mysite.models import User
from mysite.tools import myprint
import os
from django.contrib.auth import login, authenticate

API_UID = os.getenv('42_API_UID')
API_SECRET = os.getenv('42_API_SECRET')

# Create your views here.

def generate_state(length=32):
	letters = string.ascii_letters + string.digits
	return ''.join(random.choice(letters) for _ in range(length))


def api(request):
	redirect_uri = "http://127.0.0.1:8000/api/callback"
	scope = "public"
	response_type = "code"
	state = generate_state()  # Generate an unguessable random string
	request.session['oauth_state'] = state # =keep state for verification

	authorize_url = (
		"https://api.intra.42.fr/oauth/authorize?"
		f"client_id={API_UID}&"
		f"redirect_uri={redirect_uri}&"
		f"scope={scope}&"
		f"response_type={response_type}&"
		f"state={state}"
	)

	# Redirect user to the authorization endpoint
	return redirect(authorize_url)



def callback(request):
	code = request.GET.get('code')
	state = request.GET.get('state')

	if (state != request.session.pop('oauth_state')):
		return HttpResponse("State does not match!")

	token_url = "https://api.intra.42.fr/oauth/token"
	redirect_uri = "http://127.0.0.1:8000/api/callback"  # Replace with your actual redirect URI

	data = {
		'grant_type': 'authorization_code',
		'client_id': API_UID,
		'client_secret': API_SECRET,
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

		image_link = user_data['image']['link']
		# creating User object with data from intra api
		if User.objects.filter(username=user_data['login']).count() > 0:
			pass
		else:
			user = User(
				username=user_data['login'],
				email=user_data['email'],
				first_name=user_data['first_name'],
				last_name=user_data['last_name'],
				image_link=image_link)
			user.save()

		# myprint("adding login to session")
		request.session['login'] = user_data['login']
		login(request, User.objects.get(username=user_data['login']))


		return HttpResponse('<script type="text/javascript">window.close()</script>')
		# return

	except requests.exceptions.HTTPError as http_err:
		return HttpResponse(f"HTTP error occurred: {http_err}", status=response.status_code)

	except requests.exceptions.RequestException as req_err:
		return HttpResponse(f"Request error occurred: {req_err}")

	except ValueError as val_err:
		return HttpResponse(f"Value error occurred: {val_err}")

	except Exception as err:
		return HttpResponse(f"Error occurred: {err}")

	return HttpResponse("Unknown error occurred", status=500)
