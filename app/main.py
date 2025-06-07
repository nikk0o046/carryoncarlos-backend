import os
import logging
from google.cloud import logging as cloudlogging
#client = cloudlogging.Client()
#client.setup_logging(log_level=logging.DEBUG) 
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO) # for local testing
logger = logging.getLogger(__name__) # for local testing

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from phoenix.otel import register

# Tracing must be initialized before instrumented modules or libraries (e.g. OpenAI) are imported
load_dotenv()
tracer_provider = register(
    protocol="http/protobuf",
    project_name="carryon-carlos",
    batch=True,
)
tracer = tracer_provider.get_tracer(__name__)

from input_parser import input_parser
from params.destination import create_destination_params
from params.time import create_time_params
from params.duration import create_duration_params
from params.other import create_other_params
from api.make_API_request import make_API_request
from api.kiwi_output_parser import extract_info

app = FastAPI(title="Carry-on Carlos API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/search_flights')
@tracer.chain
async def search_flights(request: Request, customer_id: str | None = None):
    try:
        user_id = customer_id or 'Not Provided'
        request_body = await request.json()
        
        user_request = request_body.get('user_request', 'Not Provided')
        selectedCityID = request_body.get('selectedCityID', 'Not Provided')
        cabinClass = request_body.get('cabinClass', 'Not Provided')
        travelers = request_body.get('travelers', 'Not Provided')

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
            raise HTTPException(status_code=500, detail="API request failed. Please try again later.")

        flights_info = extract_info(response_data, user_id)
        if not flights_info:  # If no flights were found
            raise HTTPException(status_code=404, detail="No flights found matching your request.")
        return flights_info

    except KeyError as e:
        logger.exception("[UserID: %s] An error occurred: %s. The key doesn't exist in the dictionary.", user_id, e)
        raise HTTPException(status_code=400, detail=f"An error occurred: {e}. The key doesn't exist in the dictionary.")
    except Exception as e:
        logger.exception("[UserID: %s] An unexpected error occurred: %s", user_id, e)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

# Run the app
if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 8080))
    uvicorn.run(app, host='0.0.0.0', port=port)