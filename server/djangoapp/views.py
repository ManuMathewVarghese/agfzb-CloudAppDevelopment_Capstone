from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request, get_dealers_by_state, get_dealer_by_id
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)
dealership_url = "https://madavanamanu-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/"
review_url = "https://madavanamanu-5000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/"

# Create your views here.
def index(request):
    return render(request, 'djangoapp/index.html')

# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')
# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("djangoapp:index", permanent=True)
        else:
            context["message"] = "Login Unsuccessful. Try again!"
            return render(request, "djangoapp/index.html", context)
    return redirect("djangoapp:index", permanent=True)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect("djangoapp:index")

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user = None
        try:
            user = User.objects.get(username=username)
        except: pass
        if user:
            context["message"] = "User already exists!"
        else: 
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
    return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
# def get_dealerships(request):
#     context = {}
#     if request.method == "GET":
#         return render(request, 'djangoapp/index.html', context)

def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = dealership_url + "dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context["dealerships"] = dealerships
    return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    url = dealership_url + "dealerships/get"
    context["dealer"] = get_dealer_by_id(url, dealer_id)[0]
    if request.method == "GET":
        url = review_url + "get_reviews"
        dealer_reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context["dealer_reviews"] = dealer_reviews
    return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    url = dealership_url + "dealerships/get"
    context["dealer"] = get_dealer_by_id(url, dealer_id)[0]
    if request.user.is_authenticated and request.method == "POST":
        review = {}
        review["time"] = datetime.utcnow().isoformat()
        review["id"] = dealer_id
        review["dealership"] = dealer_id
        review["review"] = request.POST["content"]
        review["name"] = request.user.username
        if request.POST["purchasedate"]:
            review["purchase_date"] = request.POST["purchasedate"].split("-")[0]
        if request.POST["car"]:
            car=request.POST["car"].split("-")
            review["car_make"] = car[1]
            review["car_model"] = car[0]
            review["car_year"] = car[2]
        url = review_url + "post_review"
        print(review)
        json_payload = json.dumps({"review": review}) 
        result = post_request(url,json_payload=json_payload)
        if result:
           return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
    return render(request, 'djangoapp/add_review.html', context)
