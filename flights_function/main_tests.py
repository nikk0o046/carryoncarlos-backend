import requests
import json
from destination_params import create_destination_params
from time_params import create_time_params
from duration_params import create_duration_params
from data.test_cases import test_cases

# URL of your backend service
BASE_URL = "http://localhost:8080/search_flights"

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


def filter_test_cases(test_cases, indices):
    # If a slice is provided
    if isinstance(indices, slice):
        return test_cases[indices]
    # If a list of indices is provided
    return [test_cases[i-1] for i in indices]  # Subtracting 1 because list indices start from 0


def run_tests(func_name=None, indices=None):
    # Get the filtered test cases
    cases_to_run = filter_test_cases(test_cases, indices) if indices else test_cases

    for test_case in cases_to_run:
        print(f"Test case {test_case['test_case_number']}: {test_case['user_request']}")
        
        if func_name:
            test_function(func_name, test_case)
        else:
            headers = {
                "Content-Type": "application/json",
                "Customer-ID": f"TestUser-{test_case['test_case_number']}"  # Using test_case_number for unique user IDs
            }
            
            response = requests.post(BASE_URL, headers=headers, data=json.dumps(test_case))
            status_code = response.status_code
            response_data = response.json()
        
            print(f"Test case {test_case['test_case_number']}: {test_case['user_request']}")
            print(f"Status Code: {status_code}")
            print(f"Response: {response_data}")
            
        print("-" * 40)


run_tests("create_destination_params", indices=[33, 35, 40, 41, 42, 43, 45, 48, 49, 51]) # Using list notation for desired test cases
#run_tests("create_destination_params", indices=slice(33, None)) # Using slice notation for the first three test cases

