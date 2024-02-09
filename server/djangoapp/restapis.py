import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def post_request(url, json_payload, **kwargs):
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        print("Network exception occurred")
    return True

def analyze_review_sentiments(dealerreview):
    url = "https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/bc0d3cb7-5835-4699-9185-2e5e9a4567c4"
    api_key = "FdLq9E7GfjEZe7-hv_wdIt9qFP_rtNZAPFGpg2TrDL9M"
    version = '2024-02-08'
  
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version=version,authenticator=authenticator)

    natural_language_understanding.set_service_url(url)

    response = natural_language_understanding.analyze(
        text=dealerreview,
        features=Features(sentiment= SentimentOptions()),
    ).get_result()
    sentiment = response["sentiment"]["document"]["label"]
    return sentiment
  

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            print("Dealer",dealer_doc)
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, id=dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        dealer_reviews = json_result
        
        # For each dealer object
        for dealer_review in dealer_reviews:
            # Get its content in `doc` object
            dealer_doc = dealer_review
            print("Dealer Review",dealer_doc)
            # Create a CarDealer object with values in `doc` object
            dealer_review_obj = DealerReview(
                dealership=dealer_doc["dealership"], 
                name=dealer_doc["name"], 
                review=dealer_doc["review"], 
                purchase=dealer_doc["purchase"], 
                car_make= 'H', 
                car_model= 'G', 
                car_year= 2023,
                sentiment= analyze_review_sentiments(dealer_doc["review"]),
                id=dealer_review["id"],
                #purchase_date
            )
            results.append(dealer_review_obj)
    return results
