import os
import logging
logger = logging.getLogger(__name__)

from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
# retrieve the OPENAI_API_KEY from environment variable
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

def create_time_params(user_request):
    logger.info("Creating time parameters...")

    #initialize the openai model
    chat = ChatOpenAI(temperature=0, openai_api_key = OPENAI_API_KEY)

    #create the prompt templates
    system_template = """/
    ANSWER INSTRUCTIONS:
    The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "\`\`\`json" and "\`\`\`":

    ```json
    {{
        "key1": value1  // Define relevant values  
        "key2": value2 
    }}
    ``` 

    API DOCUMENTATION:
    date_from *
    departure date (dd/mm/yyyy). Use parameters date_from and date_to to define the range for the outbound flight departure.
    For example, parameters 'date_from=01/04/2021' and 'date_to=03/04/2021' mean that the departure can be anytime between the specified dates, i.e. on 01/04, 02/04 or 03/04.
    For the dates of the return flights, use the 'nights_in_dst_from' and 'nights_in_dst_to' parameters.
    Example : 01/04/2021
    01/04/2021

    date_to *
    departure date (dd/mm/yyyy). Use parameters date_from and date_to to define the range for the outbound flight departure.
    Example : 03/04/2021
    nights_in_dst_from
    integer
    the minimal length of stay in the destination given in the fly_to parameter.
    Example : 2

    nights_in_dst_to
    integer
    the maximal length of stay in the destination given in the fly_to parameter.

    Either both parameters 'nights_in_dst_to' and 'nights_in_dst_from' have to be specified or none of them.
    Example : 3

    fly_days
    the list of week days for the flight, where 0 is Sunday, 1 is Monday, etc.
    You can include more days than one, e.g. '&fly_days=0&fly_days=1&fly_days=2&...&fly_days=6'

    fly_days_type
    used to specify whether the fly_days day is for an arrival or a departure flight.
    Available values : departure, arrival

    ret_fly_days
    the list of week days for the flight, where 0 is Sunday, 1 is Monday, etc.
    URL encoded format for all days: '&ret_fly_days=0&ret_fly_days=1&ret_fly_days=2&...&ret_fly_days=6'

    ret_fly_days_type
    type of set ret_fly_days; It  is used to specify whether the flight is an arrival or a departure.
    Available values : departure, arrival

    For time related parameters below, only use time in whole hours, not minutes; 11:00 means 11AM, 23:00 means 11PM).

    dtime_from
    result filter, min. departure time.
    dtime_to
    result filter, max departure time.
    atime_from
    result filter, min arrival time.
    atime_to
    result filter, max arrival time.
    ret_dtime_from
    result filter, min dep. time of the returning flight.
    ret_dtime_to
    result filter, max dep. time of the returning flight.
    ret_atime_from
    result filter, min arrival time of the returning flight.
    ret_atime_to
    result filter, min arrival time of the returning flight.

    USER INTERACTIONS:
    User request: I want a weekend getaway in Paris in September. I get off work on Friday around 3pm.
    Thought: Flight dates to/from should be set to September. Because it is a weekend getaway, the user probably wants a departure on Friday and want to stay for two nights. Also, because they get off work at 3pm, they probably can’t make it to a flight departing before 5pm. Since the user will be spending just the weekend, they don’t want a flight that departures very late on Friday or very early on Sunday. Also, as they probably have work on Monday, having a departure very late on Sunday would likely be annoying.
    Flight time query:
    ```json
    {{
        'date_from': '01/09/2023',
        'date_to': '30/09/2023',
        'fly_days': 5,
        'fly_days_type': 'departure',
        'dtime_from': '17:00',
        'dtime_to': '20:00',
        'nights_in_dst_from': 2,
        'nights_in_dst_to': 2,
        'ret_fly_days': 0,
        'ret_fly_days_type': 'departure',
        'ret_dtime_from': '12:00',
        'ret_dtime_to': '18:00',
    }}
    ```
    User request: I’m on vacation from 14th of March to 18th of April. I want to go abroad for about a week.
    Thought: The “date_from” variable should be set from 14th of March to 10th of April, so that the whole trip can be done within the timeframe. The user wants the trip to last about a week, so nights in destination should be from 6 to 8 days. As the user is on vacation, it probably doesn’t matter on which days of the week they are flying or at what time.
    Flight time query:
    ```json
    {{
        'date_from': '14/03/2023',
        'date_to': '10/04/2023',
        'nights_in_dst_from': 6,
        'nights_in_dst_to': 8,
    }}
    ```
    User request: I want to go for a long weekend trip in October. I can get either Friday or Monday off from work.
    Thought: A long weekend trip usually consists of three days. Given the user can take either Friday or Monday off, the possible travel days would be Thursday, Friday, Saturday, Sunday or Monday. Since the departure date is in October, the "date_from" and "date_to" parameters should cover the whole month. The "nights_in_dst_from" and "nights_in_dst_to" parameters should both be set to 3 to match the desired length of stay. The user didn't provide specific information about their work schedule or preferred flight times, we don't have clear constraints for the departure and arrival times. However, we can make reasonable assumptions that would generally suit most working professionals.
    Assuming that the user works a typical 9-5 job, they might prefer to leave in the evening on their departure day to avoid taking additional time off work. We could set the "dtime_from" to be after their work, say 18:00 (6PM), and leave "dtime_to" open to accommodate late flights.
    For the return, the user needs to be back for work on Tuesday, so a late return on Monday may be inconvenient. We might set the "ret_dtime_to" as 20:00 (8PM) to ensure they're not getting back too late.
    Flight time query:
    ```json
    {{
        'date_from': '01/10/2023',
        'date_to': '31/10/2023',
        'nights_in_dst_from': 3,
        'nights_in_dst_to': 3,
        'fly_days': [4, 5],
        'dtime_from': '18:00',
        'ret_fly_days': [0, 1],
        'ret_dtime_to': '20:00',
    }}
    ```"""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """User request: {user_request}
    Thought: """
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    #request the response from the model
    openai_response = chat(
        chat_prompt.format_prompt(
            user_request=user_request
        ).to_messages()
    )
    logger.info(str(openai_response.content))

    # Extract the json string using regular expressions
    import re
    import json
    json_str = re.search(r'\{.*\}', openai_response.content, re.DOTALL).group()

    # Convert the json string to a Python dictionary
    time_params = json.loads(json_str)
    logger.info("Time parameters created: %s", time_params)

    return time_params
