import logging
import time

from openai import AsyncOpenAI
from opentelemetry import trace

from app.constants import OPENAI_MODEL
from app.models.openai_responses import DurationParamsResponse

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)
openai_client = AsyncOpenAI()


@tracer.chain
async def create_duration_params(user_request: str, selected_city_id: str, user_id: str) -> dict:
    """
    This function takes the user request, the selected city ID and the user ID and returns the duration parameters.

    Args:
        user_request (str): The user request.
        selected_city_id (str): The selected city ID.
        user_id (str): The user ID.

    Returns:
        dict: The duration parameters.
    """
    start_time = time.time()
    logger.debug("[UserID: %s] Creating duration parameters...", user_id)

    # Create the prompt templates
    system_template = """You're an intelligent AI agent, and your job is to create search parameters about the flight
duration, stopovers, and stopover duration.

INSTRUCTIONS:
When creating flight search parameters based on user info, consider the following:

Specified Flight Preferences: Prioritize user-specific requests, like "direct flights."
Trip Distance:
Short Haul: Favor direct routes as layovers can extend short trips unnecessarily.
Long Haul: Allow more layovers, but balance their number and duration.
Trip Duration:
Short Trips: Prioritize speed to maximize time at the destination.
Long Trips: Consider comfort and minimize unnecessary layovers.
Availability of Flights:
Major Hubs: Expect numerous direct flight options.
Less Popular Routes: Optimize for shortest total travel time and feasible connections.
Use these parameters:

max_sector_stopovers: Maximum number of stopovers per sector.
stopover_to: Maximum length of a stopover (e.g., "4:00" means 4 hours). Aim to keep under "5:00".
max_fly_duration: Maximum itinerary duration, including stopovers. Aim to keep short.

Include your reasoning in the "reasoning" field and only set parameters that are relevant."""

    # example 1
    user_example1 = """Origin: Madrid
    Info: Origin: Madrid, ES | Destination: Barcelona, ES | Departure: Next month | Duration: Weekend"""

    bot_example1 = '{"reasoning": "Short-haul Madrid to Barcelona weekend trip. Direct flights ideal from major hubs.", "max_sector_stopovers": 0}'

    # example 2
    user_example2 = """Origin: Helsinki
    Info: Origin: Helsinki, FI | Destination: South America | Departure: January | Duration: 2 weeks | Flights: Any"""

    bot_example2 = '{"reasoning": "Long-haul Helsinki to South America with flexibility. Allow layovers but limit duration for comfort.", "max_fly_duration": 20, "max_sector_stopovers": 2, "stopover_to": "5:00"}'

    # example 3
    user_example3 = """Origin: New York
    Info: "Origin: New York, US | Destination: Sydney, AU | Departure: March | Duration: 1 week | Flights: direct"""

    bot_example3 = '{"reasoning": "User wants direct flights. Set max_sector_stopovers to 0.", "max_sector_stopovers": 0}'

    human_template = f"Origin: {selected_city_id}\nInfo: {user_request}"

    message_list = [
        {"role": "system", "content": system_template},
        {"role": "user", "content": user_example1},
        {"role": "assistant", "content": bot_example1},
        {"role": "user", "content": user_example2},
        {"role": "assistant", "content": bot_example2},
        {"role": "user", "content": user_example3},
        {"role": "assistant", "content": bot_example3},
        {"role": "user", "content": human_template},
    ]

    response = await openai_client.beta.chat.completions.parse(
        model=OPENAI_MODEL,
        temperature=0,
        messages=message_list,
        response_format=DurationParamsResponse,
    )
    parsed = response.choices[0].message.parsed

    logger.debug("[UserID: %s] Duration parameters response: %s", user_id, parsed)

    # Exclude None values and the reasoning field from the output
    duration_params = parsed.model_dump(exclude_none=True, exclude={"reasoning"})

    logger.debug("[UserID: %s] Duration created: %s", user_id, duration_params)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.debug("[UserID: %s] Function execution time: %s seconds", user_id, elapsed_time)

    return duration_params
