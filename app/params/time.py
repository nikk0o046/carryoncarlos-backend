import logging
import time
from datetime import datetime, timedelta

from openai import OpenAI
from opentelemetry import trace

from app.settings import OPENAI_MODEL

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)
openai_client = OpenAI()


@tracer.chain
def create_time_params(user_request: str, user_id: str) -> dict:
    """
    This function takes the user request and the user ID and returns the time parameters.

    Args:
        user_request (str): The user request.
        user_id (str): The user ID.

    Returns:
        dict: The time parameters.
    """

    start_time = time.time()  # start timer to log it later
    logger.debug("[UserID: %s] Creating time parameters...", user_id)
    current_date_unformatted = datetime.now()
    current_date = f"{current_date_unformatted:%d/%m/%Y}"

    # create the prompt templates
    system_template = r"""API DOCUMENTATION:
departure_date_from, departure_date_to: Range for outbound flight departure (dd/mm/yyyy). These must be included. If not provided, you must make an assumption.

nights_in_dst_from, nights_in_dst_to: Minimum and maximum stay length at the destination (in nights). Only exclude these if the user is looking for a one-way trip. If not provided, you must make an assumption.

fly_days, ret_fly_days: List of preferred days for outbound and return flights (0=Sunday, 1=Monday, ... 6=Saturday). 

fly_days_type, ret_fly_days_type: Specifies if fly_days/ret_fly_days is for an arrival or a departure flight.

If the user looks for specific dates, set departure_date_from and departure_date_to to a specific date, and match nights_in_dst_from and nights_in_dst_to so that the return day will be correct.

ANSWER INSTRUCTIONS:
Your task is to create parameters specified above based on user information. The parameters will be forwarded to another assistant, who uses them to search flights. Do not come up with any other parameters.
The output should include both:
1) Thought: Thinking out loud about the user's needs and the task.
2) Markdown code snippet formatted in the following schema, including the leading and trailing "\`\`\`json" and "\`\`\`":

```json
{
    "key1": value1  // Define relevant values. Only use keys mentioned in the API documentation. 
    "key2": value2
}
```"""

    human_template = f"Current date: {current_date}\nInfo: {user_request}"

    message_list = [
        {"role": "system", "content": system_template},
        {"role": "user", "content": human_template},
    ]

    response = openai_client.chat.completions.create(
        model=OPENAI_MODEL,
        temperature=0,
        messages=message_list,
    )
    response_content = response.choices[0].message.content

    logger.debug("[UserID: %s] OpenAI response content: %s", user_id, str(response_content))

    # Extract the json string using regular expressions
    import json
    import re

    json_str = re.search(r"\{.*\}", response_content, re.DOTALL).group()

    # Convert the json string to a Python dictionary
    logger.debug("[UserID: %s] json_str: %s", user_id, json_str)
    time_params = json.loads(json_str)

    # Edit date_from keys. Kiwi API excects "date_from" instead of "departure_date_from", and the same for "date_to". "departure_date_from" and "departure_date_to" were used for model training, because it did not confuse them with the length of the trip, like it sometimes did with "date_from" and "date_to".
    if "departure_date_from" in time_params:
        time_params["date_from"] = time_params.pop("departure_date_from")

    if "departure_date_to" in time_params:
        time_params["date_to"] = time_params.pop("departure_date_to")

    # time_params = adjust_dates(time_params, user_id) # Check if dates are in the past. If they are, add a year.
    logger.debug("[UserID: %s] Time parameters created: %s", user_id, time_params)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.debug("[UserID: %s] Function execution time: %s seconds", user_id, elapsed_time)

    return time_params


@tracer.chain
def adjust_dates(time_params: dict, user_id: str) -> dict:
    """
    This function takes the time parameters and the user ID and adjusts the dates if they are in the past.

    Args:
        time_params (dict): The time parameters.
        user_id (str): The user ID.

    Returns:
        dict: The time parameters.
    """

    # Extract the dates from the parameters dictionary
    date_from_str = time_params["date_from"]
    date_to_str = time_params["date_to"]

    # Parse the dates into datetime objects
    date_format = "%d/%m/%Y"
    date_from = datetime.strptime(date_from_str, date_format)
    date_to = datetime.strptime(date_to_str, date_format)

    # Get the current date
    current_date = datetime.now()

    # If both dates are in the past, add one year to both
    if date_from < current_date and date_to < current_date:
        date_from += timedelta(days=365)
        date_to += timedelta(days=365)

        # Update the dictionary with the new dates
        time_params["date_from"] = date_from.strftime(date_format)
        time_params["date_to"] = date_to.strftime(date_format)

        # Log a warning
        logger.warning(
            "[UserID: %s] Both dates were in the past. Adjusted them to: %s - %s",
            user_id,
            time_params["date_from"],
            time_params["date_to"],
        )

    return time_params
