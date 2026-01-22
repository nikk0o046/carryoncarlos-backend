import json
import logging
import re
import time

from openai import OpenAI
from opentelemetry import trace

from app.settings import OPENAI_MODEL

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)
openai_client = OpenAI()


@tracer.chain
def create_duration_params(user_request: str, selected_city_id: str, user_id: str) -> dict:
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
    system_template = r"""You're an intelligent AI agent, and your job is to create search parameters about the flight
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
stopover_to: Maximum length of a stopover (e.g., 4:00 means 4 hours). Aim to keep under 5:00.
max_fly_duration: Maximum itinerary duration, including stopovers. Aim to keep short.
ANSWER INSTRUCTIONS:
Provide:

1) Thought: Detail your reasoning briefly.
2) Markdown code snippet formatted in the following schema, including the leading
and trailing "\`\`\`json" and "\`\`\`":

```json
{
    "key1": value1  // Define relevant values. Only use keys mentioned in the API documentation.
    "key2": value2
}
    ```"""

    # example 1
    user_example1 = """Origin: Madrid
    Info: Origin: Madrid, ES | Destination: Barcelona, ES | Departure: Next month | Duration: Weekend"""

    bot_example1 = """Thought: Considering the short-haul nature of Madrid to Barcelona and the short duration of the
trip (weekend), direct flights would be ideal.
Major hubs like Madrid and Barcelona have numerous direct flight options.
    ```json
    {
        "max_sector_stopovers": 0
    }
    ```"""

    # example 2
    user_example2 = """Origin: Helsinki
    Info: Origin: Helsinki, FI | Destination: South America | Departure: January | Duration: 2 weeks | Flights: Any"""

    bot_example2 = """Thought: The long-haul nature of Helsinki to South America, combined with the user's flexibility
for any flights, suggests that we should allow some layovers.
However, we'll aim to optimize for comfort by limiting lengthy stopovers and excessive travel time.
    ```json
    {
        "max_fly_duration": 20,
        "max_sector_stopovers": 2,
        "stopover_to": "5:00"
    }
    ```"""

    # example 3
    user_example3 = """Origin: New York
    Info: "Origin: New York, US | Destination: Sydney, AU | Departure: March | Duration: 1 week | Flights: direct"""

    bot_example3 = """Thought: The user wants direct flights, so we set max_sector_stopovers to 0.
We omit stopover_to and max_fly_duration for direct flights.
     ```json
    {
        "max_sector_stopovers": 0
    }
    ```"""

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

    response = openai_client.chat.completions.create(
        model=OPENAI_MODEL,
        temperature=0,
        messages=message_list,
    )
    response_content = response.choices[0].message.content

    logger.debug("[UserID: %s] Duration parameters response: %s", user_id, response_content)

    # Extract the json string using regular expressions
    json_str = re.search(r"\{.*\}", response_content, re.DOTALL).group()

    # Convert the json string to a Python dictionary
    logger.debug("[UserID: %s] json_str: %s", user_id, json_str)
    duration_params = json.loads(json_str)
    logger.debug("[UserID: %s] Duration created: %s", user_id, duration_params)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.debug("[UserID: %s] Function execution time: %s seconds", user_id, elapsed_time)

    return duration_params
