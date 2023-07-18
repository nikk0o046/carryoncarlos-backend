from flask import Flask, request, jsonify
from flask_cors import CORS

from make_API_request import make_API_request
from kiwi_output_parser import extract_info
from destination_params import create_destination_params
from time_params import create_time_params
from other_params import create_other_params

app = Flask(__name__)
CORS(app)

@app.route('/search_flights', methods=['POST'])
def search_flights():
    user_request = request.json['user_request']
    try:
        print("\nCreating destination parameters...")
        destination_query = create_destination_params(user_request)
        print("Destination parameters created: ", destination_query)

        print("\nCreating time parameters...")
        time_query = create_time_params(user_request)
        print("Time parameters created: ", time_query)

        print("\nCreating other parameters...")
        other_constraints = create_other_params()
        print("Other parameters created: ", other_constraints)

        print("\nMaking API request...")
        response_data = make_API_request(destination_query, time_query, other_constraints)
        print("API request completed.")
        if 'error' in response_data:
            print('Error in response_data: ', response_data['error'])
        else:
            print("Keys in response data: ", response_data.keys())

        print("\nExtracting information from response data...")
        flights_info = extract_info(response_data)
        print("Information extraction completed.")

        print("\nPrinting flights information...")
        for info in flights_info:
            print(info)

    except KeyError as e:
        print(f"\nAn error occurred: {e}. The key doesn't exist in the dictionary.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == '__main__':
    app.run(port=5000)