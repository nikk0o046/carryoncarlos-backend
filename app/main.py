import os
import logging
from google.cloud import logging as cloudlogging
#client = cloudlogging.Client()
#client.setup_logging(log_level=logging.DEBUG) 
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO) # for local testing
logger = logging.getLogger(__name__) # for local testing

from flask import Flask, request, jsonify
from flask_cors import CORS

from input_parser import input_parser
from params.destination import create_destination_params
from params.time import create_time_params
from params.duration import create_duration_params
from params.other import create_other_params
from api.make_API_request import make_API_request
from api.kiwi_output_parser import extract_info

app = Flask(__name__)
CORS(app)

@app.route('/search_flights', methods=['POST'])
def search_flights():
    try:
        user_id = request.headers.get('Customer-ID', 'Not Provided')
        requestBody = request.json

        user_request = requestBody.get('user_request', 'Not Provided')
        selectedCityID = requestBody.get('selectedCityID', 'Not Provided')
        cabinClass = requestBody.get('cabinClass', 'Not Provided')
        travelers = requestBody.get('travelers', 'Not Provided')

        logger.info("[UserID: %s] user_request: %s", user_id, user_request)
        logger.debug("[UserID: %s] selectedCityID: %s", user_id, selectedCityID)
        logger.debug("[UserID: %s] cabinClass: %s", user_id, cabinClass)
        logger.debug("[UserID: %s] travelers: %s", user_id, travelers)

        parsed_request = input_parser(user_request, selectedCityID, user_id)

        destination_params = create_destination_params(parsed_request, user_id) # Set destination(s)
        time_params = create_time_params(parsed_request, user_id) # Set when
        duration_params = create_duration_params(parsed_request, selectedCityID, user_id) # Set stopovers and journey duration
        other_constraints = create_other_params(selectedCityID, cabinClass, travelers, user_id) # Harcoded and user selected variables

        response_data = make_API_request(destination_params, time_params, duration_params, other_constraints, user_id)
        if response_data is None:  # If API request failed
            return jsonify({"error": "API request failed. Please try again later."}), 500

        flights_info = extract_info(response_data, user_id)
        if not flights_info:  # If no flights were found
            return jsonify({"error": "No flights found matching your request."}), 404
        return jsonify(flights_info), 200  # If everything went fine

    except KeyError as e:
        logger.exception("[UserID: %s] An error occurred: %s. The key doesn't exist in the dictionary.", user_id, e)
        return jsonify({"error": f"An error occurred: {e}. The key doesn't exist in the dictionary."}), 400
    except Exception as e:
        logger.exception("[UserID: %s] An unexpected error occurred: %s", user_id, e)
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500
    

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)