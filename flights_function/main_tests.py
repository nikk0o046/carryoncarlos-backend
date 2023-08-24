import requests
import json
from destination_params import create_destination_params
from time_params import create_time_params
from duration_params import create_duration_params

# URL of your backend service
BASE_URL = "http://localhost:8080/search_flights"

# 10 example test cases
test_cases = [
    {
        "user_request": "Origin: Oslo, NO | Destination: Riga | Departure: October, any Friday | Duration: 2 nights",
        "selectedCityID": "oslo_no",
        "cabinClass": "economy",
        "travelers": {"adults": 1, "children": 0, "infants": 0}
    },
    {
        "user_request": "Origin: Stockholm, SE | Destination: Frankfurt | Departure: October 12th | Return: October 15th",
        "selectedCityID": "stockholm_se",
        "cabinClass": "economy",
        "travelers": {"adults": 1, "children": 0, "infants": 0}
    },
    {
        "user_request": "Origin: Copenhagen, DK | Destination: Best surfing spots in Portugal | Departure: Spring 2024 | Duration: 1 week",
        "selectedCityID": "copenhagen_dk",
        "cabinClass": "economy",
        "travelers": {"adults": 1, "children": 0, "infants": 0}
    },
    {
        "user_request": "Origin: Amsterdam, NL | Destination: Valencia, Spain | Departure: 1st September | Return: 7th September | Passengers: 2 adults",
        "selectedCityID": "amsterdam_nl",
        "cabinClass": "economy",
        "travelers": {"adults": 2, "children": 0, "infants": 0}
    },
    {
        "user_request": "Origin: Brussels, BE | Destination: Casablanca, Morocco | Departure: September 7th | Return: September 23rd | Passengers: 3 adults",
        "selectedCityID": "brussels_be",
        "cabinClass": "economy",
        "travelers": {"adults": 3, "children": 0, "infants": 0}
    },
    {
        "user_request": "Origin: Dublin, IE | Destination: East Coast US (Boston/Washington D.C.) | Departure: September-October | Duration: 12-16 days",
        "selectedCityID": "dublin_ie",
        "cabinClass": "economy",
        "travelers": {"adults": 1, "children": 0, "infants": 0}
    },
    {
        "user_request": "Origin: Paris, FR | Destination: Greek Isles | Departure: Flexible | Duration: 7-12 days",
        "selectedCityID": "paris_fr",
        "cabinClass": "economy",
        "travelers": {"adults": 1, "children": 0, "infants": 0}
    },
    {
        "user_request": "Origin: Berlin, DE | Destination: Tropical destination in Asia | Departure: Mid-November to December | Duration: Approx. 10 nights",
        "selectedCityID": "berlin_de",
        "cabinClass": "economy",
        "travelers": {"adults": 1, "children": 0, "infants": 0}
    },
    {
        "user_request": "Origin: Tampere, FI | Destination: City in Eastern Europe | Departure: Evening | Duration: 2 nights | Occasion: Bachelors party",
        "selectedCityID": "tampere_fi",
        "cabinClass": "economy",
        "travelers": {"adults": 1, "children": 0, "infants": 0}
    },
    {
        "user_request": "Origin: Madrid, ES | Destination: Tropical snorkeling destination | Departure: Before Summer 2024 | Duration: Approx. 1 week",
        "selectedCityID": "madrid_es",
        "cabinClass": "economy",
        "travelers": {"adults": 1, "children": 0, "infants": 0}
    }
]

def test_function(func_name, test_case):
    user_id = "TestUser"  # Assuming this is how you've structured your user ID. Modify accordingly.
    if func_name == "create_destination_params":
        result = create_destination_params(test_case["user_request"], test_case["selectedCityID"], user_id)
    elif func_name == "create_time_params":
        result = create_time_params(test_case["user_request"], user_id)
    elif func_name == "create_duration_params":
        result = create_duration_params(test_case["user_request"], test_case["selectedCityID"], user_id)
    else:
        raise ValueError("Invalid function name provided.")
    
    print(result)

def run_tests(func_name=None):
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test case {i}: {test_case['user_request']}")
        
        if func_name:
            test_function(func_name, test_case)
        else:
            # Put your previous code here for testing the whole function
            headers = {
            "Content-Type": "application/json",
            "Customer-ID": f"TestUser-{i}"  # Just to have unique user IDs for each test
            }
            
            response = requests.post(BASE_URL, headers=headers, data=json.dumps(test_case))
            status_code = response.status_code
            response_data = response.json()
        
            print(f"Test case {i}: {test_case['user_request']}")
            print(f"Status Code: {status_code}")
            print(f"Response: {response_data}")
            
        
        print("-" * 40)


run_tests("create_time_params") # input the function name you want to test. Leave blank to test the whole app (it has to be running).
