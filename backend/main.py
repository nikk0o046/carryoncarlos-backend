import os
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

from flask import Flask, request, jsonify
from flask_cors import CORS

from destination_params import create_destination_params
from time_params import create_time_params
from other_params import create_other_params
from make_API_request import make_API_request
from kiwi_output_parser import extract_info

app = Flask(__name__)
CORS(app)

@app.route('/search_flights', methods=['POST'])
def search_flights():
    try:
        user_request = request.json['user_request']
        logger.info("user_request: %s", user_request)
        destination_query = create_destination_params(user_request)
        time_query = create_time_params(user_request)
        other_constraints = create_other_params()

        response_data = make_API_request(destination_query, time_query, other_constraints)
        if response_data is None:  # If API request failed
            return jsonify({"error": "API request failed. Please try again later."}), 500

        flights_info = extract_info(response_data)
        if not flights_info:  # If no flights were found
            return jsonify({"error": "No flights found matching your request."}), 404
        return jsonify(flights_info), 200  # If everything went fine

    except KeyError as e:
        logger.exception("An error occurred: %s. The key doesn't exist in the dictionary.", e)
        return jsonify({"error": f"An error occurred: {e}. The key doesn't exist in the dictionary."}), 400
    except Exception as e:
        logger.exception("An unexpected error occurred: %s", e)
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500
    

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)