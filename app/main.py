from httpx import AsyncClient
import logging
import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from openinference.instrumentation.openai import OpenAIInstrumentor
from phoenix.otel import register
from pydantic import BaseModel

from app.constants import KIWI_BASE_URL


# Tracing must be initialized before instrumented modules or libraries (e.g. OpenAI) are imported
load_dotenv()
tracer_provider = register(
    protocol="http/protobuf",
    project_name="carryon-carlos",
    batch=True,
)
tracer = tracer_provider.get_tracer(__name__)
OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)

from app.api.kiwi_output_parser import extract_info  # noqa: E402
from app.api.make_api_request import make_api_request  # noqa: E402
from app.input_parser import input_parser  # noqa: E402
from app.params.destination import create_destination_params  # noqa: E402
from app.params.duration import create_duration_params  # noqa: E402
from app.params.other import create_other_params  # noqa: E402
from app.params.time import create_time_params  # noqa: E402

KIWI_API_KEY = os.environ["KIWI_API_KEY"]

# client = cloudlogging.Client()
# client.setup_logging(log_level=logging.DEBUG)
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)  # for local testing
logger = logging.getLogger(__name__)  # for local testing


async def lifespan(app: FastAPI):
    async with AsyncClient(base_url=KIWI_BASE_URL, headers={"apikey": KIWI_API_KEY}) as kiwi_client:
        yield {"kiwi_client": kiwi_client}


app = FastAPI(title="Carry-on Carlos API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class FlightRequest(BaseModel):
    user_request: str
    selected_city_id: str
    cabin_class: str
    travelers: int


class LocationQuery(BaseModel):
    term: str
    locale: str = "en-US"
    location_types: str = "city"
    limit: int = 5


@app.post("/search_flights")
@tracer.chain
async def search_flights(flight_request: FlightRequest, customer_id: str | None = None):
    try:
        user_id = customer_id or "Not Provided"

        user_request = flight_request.user_request
        selected_city_id = flight_request.selected_city_id
        cabin_class = flight_request.cabin_class
        travelers = flight_request.travelers

        logger.info("[UserID: %s] user_request: %s", user_id, user_request)
        logger.debug("[UserID: %s] selected_city_id: %s", user_id, selected_city_id)
        logger.debug("[UserID: %s] cabin_class: %s", user_id, cabin_class)
        logger.debug("[UserID: %s] travelers: %s", user_id, travelers)

        parsed_request = input_parser(user_request, selected_city_id, user_id)

        destination_params = create_destination_params(parsed_request, user_id)  # Set destination(s)
        time_params = create_time_params(parsed_request, user_id)  # Set when
        duration_params = create_duration_params(
            parsed_request, selected_city_id, user_id
        )  # Set stopovers and journey duration
        other_constraints = create_other_params(
            selected_city_id, cabin_class, travelers, user_id
        )  # Harcoded and user selected variables

        response_data = make_api_request(destination_params, time_params, duration_params, other_constraints, user_id)
        if response_data is None:  # If API request failed
            raise HTTPException(status_code=500, detail="API request failed. Please try again later.")

        flights_info = extract_info(response_data, user_id)
        if not flights_info:  # If no flights were found
            raise HTTPException(status_code=404, detail="No flights found matching your request.")
        return flights_info

    except KeyError as e:
        logger.exception(
            "[UserID: %s] An error occurred: %s. The key doesn't exist in the dictionary.",
            user_id,
            e,
        )
        raise HTTPException(
            status_code=400,
            detail=f"An error occurred: {e}. The key doesn't exist in the dictionary.",
        )
    except Exception as e:
        logger.exception("[UserID: %s] An unexpected error occurred: %s", user_id, e)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")


@app.get("/health_check")
async def health_check():
    return {"status": "ok"}


@app.get("/locations/query")
async def location_query(request: Request, params: LocationQuery = Depends()):
    response = await request.app.state.kiwi_client.get("/locations/query", params=params.model_dump())
    return response.json()


# Run the app
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
