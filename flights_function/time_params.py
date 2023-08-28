import os
from datetime import datetime, timedelta
import time
import logging
logger = logging.getLogger(__name__)
import openai

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
# Set the API key and organization ID from environment variables
openai.api_key = os.environ.get('OPENAI_API_KEY')
openai.organization = os.environ.get('OPENAI_ORG_ID')

def create_time_params(user_request, user_id):
    start_time = time.time() #start timer to log it later
    logger.debug("[UserID: %s] Creating time parameters...", user_id)
    current_date_unformatted = datetime.now()
    current_date = f"{current_date_unformatted:%d/%m/%Y}"

    #create the prompt templates
    system_template = """API DOCUMENTATION:
    date_from, date_to: Range for outbound flight departure (dd/mm/yyyy). 

    nights_in_dst_from, nights_in_dst_to: Minimum and maximum stay length at the destination (in nights). Only exclude these if the user is looking for a one-way trip. Otherwise you must make an assumption.

    fly_days, ret_fly_days: List of preferred days for outbound and return flights (0=Sunday, 1=Monday, ... 6=Saturday). 

    fly_days_type, ret_fly_days_type: Specifies if fly_days/ret_fly_days is for an arrival or a departure flight. 

    dtime_from, dtime_to, ret_dtime_from, ret_dtime_to: Define the earliest and latest departure time for outbound and return flights. 

    atime_from, atime_to, ret_atime_from, ret_atime_to: Define the earliest and latest arrival time for outbound and return flights.

    ANSWER INSTRUCTIONS:
    The output should include both:
    1) Thought: Thinking out loud about the user's needs and the task.
    2) Markdown code snippet formatted in the following schema, including the leading and trailing "\`\`\`json" and "\`\`\`":

    ```json
    {{
        "key1": value1  // Define relevant values. Only use keys mentioned in the API documentation. 
        "key2": value2
    }}
    ```"""

    #example 1
    userExample1 = """Current date: 10/07/2023
    Info: Origin: London, GB | Destination: Paris, FR | Departure: Next month's Friday after 5pm | Duration: Weekend | Flights: Any"""

    botExample1 = """Answer: User wants to leave on a Friday next month (August) and stay for two nights. Outbound flight should be after 5pm, return flight should not be too late for work next day.
    ```json
    {{
        "date_from": "01/08/2023",
        "date_to": "31/08/2023",
        "fly_days": 5,
        "fly_days_type": "departure",
        "dtime_from": "17:00",
        "dtime_to": "20:00",
        "nights_in_dst_from": 2,
        "nights_in_dst_to": 2,
        "ret_fly_days": 0,
        "ret_fly_days_type": "departure",
        "ret_dtime_from": "12:00",
        "ret_dtime_to": "18:00"
    }}
    ```"""

    #example 2
    userExample2 = """Current date: 01/01/2024
    Info: Origin: San Francisco, US | Destination: Anywhere abroad | Departure: March | Duration: About a week | Flights: Any"""

    botExample2 = """Answer: setting departure dates for next March, lasting about a week which translated to 6-8 nights.
    ```json
    {{
    "date_from": "01/03/2024",
    "date_to": "31/03/2024",
    "nights_in_dst_from": 6,
    "nights_in_dst_to": 8
    }}
    ```"""

    #example 3
    userExample3 = """Current date: 10/08/2023
    Info: Origin: Los Angeles, US | Destination: Miami, US | Departure: October's Long Weekend | Duration: 3 days | Flights: After 6pm"""

    botExample3 = """Answer: Long weekend usually means three days. Possible departure days are Thursday and Friday. Possible return flight days are Sunday or Monday. Outbound flight should be after 6pm, return flight not too late for work next day.
    ```json
    {{
        "date_from": "01/10/2023",
        "date_to": "31/10/2023",
        "nights_in_dst_from": 3,
        "nights_in_dst_to": 3,
        "fly_days": [4, 5],
        "dtime_from": "18:00",
        "ret_fly_days": [0, 1],
        "ret_dtime_to": "20:00"
    }}
    ```"""

    #example 4
    userExample4 = """Current date: 10/04/2023
    Info: Origin: Chicago, US | Destination: Paris, FR | Departure: Summer | Flights: One-way"""

    botExample4 = """Answer: The user only needs an outbound flight to Paris, which should be anytime in the summer months (June, July, August). Because it is a one-way trip, nights_in_dst-parameters must be excluded. 
    ```json
    {{
        "date_from": "01/06/2023",
        "date_to": "31/08/2023"
    }}
    ```"""

    #example 5
    userExample5 = """Current date: 10/07/2023
    Info: Origin: Boston, US | Destination: Abroad | Duration: not specified | Flights: Two-way"""

    botExample5 = """Answer: The user is very vague about when they want to go or for how long. To find two-way fligths we must include nights_in_dst-parameters, so we need to make assumptions. Let's assume roughly one-week stay and look for flights in the next three months.
    ```json
    {{
        "date_from": "11/07/2023",
        "date_to": "10/10/2023",
        "nights_in_dst_from": 5,
        "nights_in_dst_to": 9
    }}
    ```"""

    human_template = f"Current date: {current_date}\nInfo: {user_request}"

    # Construct the conversation message list
    message_list = [
        {"role": "system", "content": system_template},
        {"role": "user", "content": userExample1},
        {"role": "assistant", "content": botExample1},
        {"role": "user", "content": userExample2},
        {"role": "assistant", "content": botExample2},
        {"role": "user", "content": userExample3},
        {"role": "assistant", "content": botExample3},
        {"role": "user", "content": userExample4},
        {"role": "assistant", "content": botExample4},
        {"role": "user", "content": userExample5},
        {"role": "assistant", "content": botExample5},
        {"role": "user", "content": human_template}
    ]

    # Request the response from the model
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo-0613",
      temperature=0,
      messages=message_list,
    )
    response_content = response.choices[0].message['content']

    logger.debug("[UserID: %s] OpenAI response content: %s", user_id, str(response_content))
    
    print("response_content: " + str(response_content)) # FOR LOCAL TESTING
    print("Prompt Tokens Used: " + str(response["usage"]['prompt_tokens']) + " | Completion Tokens Used: " + str(response["usage"]['completion_tokens']) + " | Total Tokens Used: " + str(response["usage"]['total_tokens']))

    # Extract the json string using regular expressions
    import re
    import json
    json_str = re.search(r"\{.*\}", response_content, re.DOTALL).group()

    # Convert the json string to a Python dictionary
    logger.debug("[UserID: %s] json_str: %s", user_id, json_str)
    time_params = json.loads(json_str)
    time_params = adjust_dates(time_params, user_id) # Check if dates are in the past. If they are, add a year.
    logger.debug("[UserID: %s] Time parameters created: %s", user_id, time_params)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.debug("[UserID: %s] Function execution time: %s seconds", user_id, elapsed_time)

    return time_params


# A helper function in case the dates are in the past
def adjust_dates(time_params, user_id):
    # Extract the dates from the parameters dictionary
    date_from_str = time_params['date_from']
    date_to_str = time_params['date_to']

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
        time_params['date_from'] = date_from.strftime(date_format)
        time_params['date_to'] = date_to.strftime(date_format)

         # Log a warning
        logger.warning("[UserID: %s] Both dates were in the past. Adjusted them to: %s - %s", user_id, time_params['date_from'], time_params['date_to'])

    return time_params

test_request = "Origin: Helsinki, FI; Destination: Vilna; Departure: October, any Friday; Duration: 2 nights"
print(create_time_params(test_request, "test_user"))