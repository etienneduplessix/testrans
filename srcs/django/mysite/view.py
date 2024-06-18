from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
import requests
import random
import string

def items_list(request):
    items = [
        {'id': 1, 'name': 'Item 1'},
        {'id': 2, 'name': 'Item 2'},
    ]
    return JsonResponse(items, safe=False)

def generate_state(length=32):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


def api(request):
    client_id = "u-s4t2ud-2bab19cc143ef78ed9f8965bfad943ab5447157ef0992e53a4cbbf0843926385"
    redirect_uri = "http://127.0.0.1:8000/api/callback"
    scope = "public"
    response_type = "code"
    state = "a_very_long_random_string"  # Generate an unguessable random string

    authorize_url = (
        "https://api.intra.42.fr/oauth/authorize?"
        f"client_id={client_id}&"
        f"redirect_uri={redirect_uri}&"
        f"scope={scope}&"
        f"response_type={response_type}&"
        f"state={state}"
    )

    return redirect(authorize_url)

from django.shortcuts import render, redirect
import requests
import random
import string

def callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    
    token_url = "https://api.intra.42.fr/oauth/token"
    client_id = "u-s4t2ud-2bab19cc143ef78ed9f8965bfad943ab5447157ef0992e53a4cbbf0843926385"
    client_secret = "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"
    redirect_uri = "http://127.0.0.1:8000/api/callback"

    data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': redirect_uri
    }
    try:
        response = requests.post(token_url, data=data)
        response.raise_for_status()

        token_data = response.json()
        access_token = token_data.get('access_token')
        
        user_url = "https://api.intra.42.fr/v2/me"
        headers = {'Authorization': f'Bearer {access_token}'}
        user_response = requests.get(user_url, headers=headers)
        user_response.raise_for_status()

        user_data = user_response.json()
        user_name = user_data['login']
        
        # Render home.html template with user_name data
        return render(request, 'home.html', {'user_name': user_name})

    except requests.exceptions.HTTPError as http_err:
        return HttpResponse(f"HTTP error occurred: {http_err}", status=response.status_code)
    
    except requests.exceptions.RequestException as req_err:
        return HttpResponse(f"Request error occurred: {req_err}")

    except ValueError as val_err:
        return HttpResponse(f"Value error occurred: {val_err}")

    except Exception as err:
        return HttpResponse(f"Error occurred: {err}")

    return HttpResponse("Unknown error occurred", status=500)


def home(request):
    return render(request, 'home.html')
