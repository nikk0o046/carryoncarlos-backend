from make_API_request import make_API_request
from kiwi_output_parser import extract_info
from parameter_functions.destination_params import create_destination_params
from parameter_functions.time_params import create_time_params
from parameter_functions.other_params import create_other_params

user_request = """I want to travel somewhere warm in Europe in October 2023 for a weekend after I get from work at 4pm.
"""
destination_query = create_destination_params()
time_query = create_time_params()
other_constraints = create_other_params()

response_data = make_API_request(destination_query, time_query, other_constraints)
flights_info = extract_info(response_data)
for info in flights_info:
    print(info)
