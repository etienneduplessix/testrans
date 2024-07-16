from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
import requests
import random
from mysite.tools import myprint
from django.http import HttpResponse, Http404
from django.conf import settings
import os
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.views.decorators.csrf import csrf_protect

def home(request):
    return render(request, 'index.html')

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def get_template(request, template_name):
    if request.method == 'GET':
        template_path = os.path.join(settings.BASE_DIR, 'mysite/templates', f'{template_name}')
        myprint("HERE: " + template_path)
        if os.path.exists(template_path):
            with open(template_path, 'r') as file:
                return HttpResponse(file.read(), content_type='text/html')
        else:
            raise Http404("Template no bueno")
    return HttpResponse(status=405)


def load_template(request, template_name):
    return redirect('/?template='+template_name)


def view_404(request, exception=None):
    # make a redirect to homepage
    # you can use the name of url or just the plain link
    return redirect('/') # or redirect('name-of-index-url')


def logout(request):
    request.session.flush()
    return redirect('/')



def callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')

    token_url = "https://api.intra.42.fr/oauth/token"
    client_id = "u-s4t2ud-2bab19cc143ef78ed9f8965bfad943ab5447157ef0992e53a4cbbf0843926385"  # Replace with your actual client_id
    client_secret = "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"  # Replace with your actual client_secret
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
