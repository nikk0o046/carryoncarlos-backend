import json

import requests

from app.params.destination import create_destination_params
from app.params.duration import create_duration_params
from app.params.time import create_time_params

# Load the test cases from the JSON file
with open("./flights_function/data/test_cases.json", "r") as file:
    test_cases = json.load(file)

# URL of your backend service
BASE_URL = "http://localhost:8080/search_flights"


def test_function(func_name: str, test_case: dict) -> None:
    """
    Test a single function with a single test case.

    Args:
        func_name (str): The name of the function to test.
        test_case (dict): The test case to run.

    Returns:
        None
    """
    user_id = "TestUser"
    if func_name == "create_destination_params":
        result = create_destination_params(test_case["user_request"], user_id)
    elif func_name == "create_time_params":
        result = create_time_params(test_case["user_request"], user_id)
    elif func_name == "create_duration_params":
        result = create_duration_params(test_case["user_request"], test_case["selectedCityID"], user_id)
    else:
        raise ValueError("Invalid function name provided.")

    print(result)


def filter_test_cases(test_cases: list[dict], indices: list[int] | slice) -> list[dict]:
    """
    Filter the test cases by their indices.

    Args:
        test_cases (list[dict]): The list of test cases to filter.
        indices (list[int] or slice): Specifies the test cases to run by their indices.

    Returns:
        list[dict]: The filtered list of test cases.
    """

    # If a slice is provided
    if isinstance(indices, slice):
        return test_cases[indices]
    # If a list of indices is provided
    return [test_cases[i - 1] for i in indices]  # Subtracting 1 because list indices start from 0


def run_tests(func_name: str | None = None, indices: list[int] | slice = None) -> None:
    """
    Execute a suite of test cases for specified functions or the entire app and print the results.
    If testing the entire app, the app should be running on localhost:8080.

    Args:
        func_name (str or None): Specifies the function to test. If not provided, tests the entire app.
        indices (list[int] or slice): Specifies the test cases to run by their indices.
        If not provided, all test cases are run.

    Examples:
    # Using list notation for desired test cases:
    run_tests("create_destination_params", indices=[33, 35, 40, 41, 42, 43, 45, 48, 49, 51])

    # Using slice notation for test cases 60 onwards:
    run_tests("create_destination_params", indices=slice(60, None))

    Returns:
        None
    """
    cases_to_run = filter_test_cases(test_cases, indices) if indices else test_cases

    for test_case in cases_to_run:
        print(f"Test case {test_case['test_case_number']}: {test_case['user_request']}")

        if func_name:
            test_function(func_name, test_case)
        else:
            headers = {
                "Content-Type": "application/json",
                "Customer-ID": f"TestUser-{test_case['test_case_number']}",  # test_case_number for unique user IDs
            }

            response = requests.post(BASE_URL, headers=headers, data=json.dumps(test_case))
            status_code = response.status_code
            response_data = response.json()

            print(f"Test case {test_case['test_case_number']}: {test_case['user_request']}")
            print(f"Status Code: {status_code}")
            print(f"Response: {response_data}")

        print("-" * 40)


run_tests("create_time_params", indices=slice(45, None))
