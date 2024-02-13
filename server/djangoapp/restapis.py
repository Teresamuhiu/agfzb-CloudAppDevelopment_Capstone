import requests
import json
# import related models here
from .models import CarDealer
from .models import DealerReview
#from .restapis import get_request
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth

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


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    # Call get_request method to fetch data
    json_result = get_request(url, **kwargs)

    dealers = []
    # Parse JSON result and create CarDealer objects
    if json_result:
        dealers_json = json_result["body"]["docs"]
        for dealer_json in dealers_json:
            dealer = CarDealer(
                address=dealer_json["address"],
                city=dealer_json["city"],
                full_name=dealer_json["full_name"],
                id=dealer_json["id"],
                lat=dealer_json["lat"],
                long=dealer_json["long"],
                short_name=dealer_json["short_name"],
                st=dealer_json["st"],
                zip=dealer_json["zip"]
            )
            dealers.append(dealer)

    return dealers


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def analyze_review_sentiments(text, api_key):
    url = "https://76466da7-2ceb-43bd-b5ca-6905ea29a608-bluemix.cloudantnosqldb.appdomain.cloud"
    params = {
        "text": text,
        "features": {"sentiment": {}},
        "return_analyzed_text": True
    }

    response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                            auth=HTTPBasicAuth('apikey', api_key))

    if response.status_code == 200:
        return response.json().get("sentiment", {}).get("document", {}).get("label", "Unknown")
    else:
        return "Unknown"



# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(dealer_id):
    url = "https://muhiutw9-5000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews?id=13"
    # Call get_request method to fetch data
    json_result = get_request(url, dealerId=dealer_id, api_key=api_key)

    dealer_reviews = []
    # Parse JSON result and create DealerReview objects
    if json_result:
        reviews_json = json_result.get("reviews", [])
        for review_json in reviews_json:
            dealer_review = DealerReview(
                dealership=review_json.get("dealership", ""),
                name=review_json.get("name", ""),
                purchase=review_json.get("purchase", ""),
                review=review_json.get("review", ""),
                purchase_date=review_json.get("purchase_date", ""),
                car_make=review_json.get("car_make", ""),
                car_model=review_json.get("car_model", ""),
                car_year=review_json.get("car_year", ""),
                sentiment=analyze_review_sentiments(review_json.get("review", ""), api_key),
                id=review_json.get("id", "")
            )
            dealer_reviews.append(dealer_review)

    return dealer_reviews



