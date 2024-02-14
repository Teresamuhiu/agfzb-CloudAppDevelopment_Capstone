from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
# from .models import related models
# from .restapis import related methods
from .restapis import get_dealers_from_cf
from .restapis import post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from datetime import datetime
import logging
import json




# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
from django.shortcuts import render

def index(request):
    return render(request, 'djangoapp/index.html')



# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('djangoapp:index'))  # Redirect to the homepage after successful login
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    return render(request, 'djangoapp/login.html')
# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...
def logout_request(request):
    logout(request)
    return redirect(reverse('djangoapp:index'))

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def signup_request(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect(reverse('djangoapp:index'))  # Redirect to the login page after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'djangoapp/registration.html', {'form': form})

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://muhiutw9-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Build a context dictionary to pass data to the template
        context = {
            'dealerships': dealerships,
        }
       # Render the template with the context data
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    # API key for Watson NLU service
    api_key = "NpjYIT4_ZFHVWNxKc88lKFutCSOW5_HRLjd_ZMZNdg3l"

    # Call get_dealer_reviews_from_cf to get reviews for the specified dealer_id
    dealer_reviews = get_dealer_reviews_from_cf(dealer_id, api_key)

     # Process sentiment analysis for each review
    for review in dealer_reviews:
        review.sentiment = analyze_review_sentiments(review.review, api_key)

   #Build a context dictionary to pass data to the template
    context = {
        'dealer_reviews': dealer_reviews,
    }

    # Return an HTTP response with the context data
    return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return HttpResponse("User is not authenticated. Please login to post a review.")

    if request.method == 'GET':
        # Query cars with the dealer id to be reviewed
        cars = get_dealers_from_cf(dealer_id)

        context = {
            'cars': cars,
        }

        return render(request, 'djangoapp/add_review.html', context)

    elif request.method == 'POST':
        # Obtain form data
        content = request.POST.get('content')
        purchasecheck = request.POST.get('purchasecheck')
        car_id = request.POST.get('car')
        purchasedate = request.POST.get('purchasedate')

        # Format review time
        review_time = datetime.utcnow().isoformat()

        # Get year from purchasedate
        purchase_year = datetime.strptime(purchasedate, '%m/%d/%Y').strftime('%Y')

        # Create a dictionary object for the review
        review = {
            "time": review_time,
            "dealership": dealer_id,
            "review": content,
            "purchase": True if purchasecheck else False,
            "car_make": "",  # Populate with actual car make
            "car_model": "",  # Populate with actual car model
            "car_year": purchase_year,
        }

        # Create a JSON payload with the review
        json_payload = {"review": review}

        # URL for posting the review
        url = "https://muhiutw9-5000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review"

        # Call the post_request method with the payload
        post_response = post_request(url, json_payload, dealerId=dealer_id)

        # Check if the post request was successful
        if post_response:
            # Redirect user to the dealer details page
            return redirect(reverse("djangoapp:dealer_details", kwargs={'dealer_id': dealer_id}))
        else:
            return HttpResponse("Failed to post the review. Try again later.")