import logging
import time

from openai import AsyncOpenAI
from opentelemetry import trace

from app.constants import OPENAI_MODEL
from app.models.openai_responses import DestinationResponse

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

openai_client = AsyncOpenAI()


@tracer.chain
async def create_destination_params(user_request: str, user_id: str) -> dict:
    """
    This function takes the user request and the selectedcityID and returns the destination parameters.

    Args:
        user_request (str): The user request.
        selectedCityID (str): The selected city ID.
        user_id (str): The user ID.

    Returns:
        dict: The destination parameters.
    """

    start_time = time.time()  # start timer to log it later
    logger.debug("[UserID: %s] Creating destination parameters...", user_id)

    system_template = """You are an advanced AI agent tasked with identifying as many potential destination airports as
possible based on user preferences. Your response should include:

1. A "reasoning" field with your initial thought process for the task.
2. An "airport_codes" field with an exhaustive list of IATA airport codes matching the criteria.

For ambiguous destinations, aim for at least 15 to 20 airport codes. Offering more options increases the chances of
finding affordable flights for the user. Focus on final destination airports only, excluding connecting airports.
Disregard any irrelevant information."""

    human_template = user_request

    message_list = [
        {"role": "system", "content": system_template},
        {"role": "user", "content": human_template},
    ]

    response = await openai_client.beta.chat.completions.parse(
        model=OPENAI_MODEL,
        temperature=0,
        messages=message_list,
        response_format=DestinationResponse,
    )
    parsed = response.choices[0].message.parsed

    logger.debug("[UserID: %s] Destination parameters response: %s", user_id, parsed)

    if parsed and parsed.airport_codes:
        destination_params = {
            "fly_to": ",".join(parsed.airport_codes),
        }
    else:
        destination_params = {}

    logger.debug("[UserID: %s] Destination parameters created: %s", user_id, destination_params)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.debug("[UserID: %s] Function execution time: %s seconds", user_id, elapsed_time)

    return destination_params
