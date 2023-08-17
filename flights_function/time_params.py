import os
from datetime import datetime, timedelta
import time
import logging
logger = logging.getLogger(__name__)

from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
)

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
# retrieve the OPENAI_API_KEY from environment variable
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def create_time_params(user_request):
    start_time = time.time() #start timer to log it later
    logger.info("Creating time parameters...")
    current_date_unformatted = datetime.now()
    current_date = f"{current_date_unformatted:%d/%m/%Y}"

    #initialize the openai model
    chat = ChatOpenAI( model="gpt-4", temperature=0, openai_api_key = OPENAI_API_KEY, openai_organization="org-aaoYoL6D18BG1Z1btni0f4i6")

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
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

    #example 1
    userExample1 = """Current date: 10/07/2023
    User: Weekend getaway in Paris next month. Off work on Friday around 3pm."""
    userExample_prompt1 = HumanMessagePromptTemplate.from_template(userExample1)

    botExample1 = """Answer: User wants to leave on a Friday next month and stay for two nights. Outbound flight should be after work (assumed 5PM), return flight should not be too late for work next day.
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
    botExample_prompt1 = AIMessagePromptTemplate.from_template(botExample1)

    #example 2
    userExample2 = """Current date: 01/01/2024
    User: On vacation next March. Want to go abroad for about a week."""
    userExample_prompt2 = HumanMessagePromptTemplate.from_template(userExample2)

    botExample2 = """Answer: The trip can be done within the vacation dates next March, lasting about a week.
    ```json
    {{
    "date_from": "01/03/2024",
    "date_to": "31/03/2024",
    "nights_in_dst_from": 6,
    "nights_in_dst_to": 8
    }}
    ```"""
    botExample_prompt2 = AIMessagePromptTemplate.from_template(botExample2)

    #example 3
    userExample3 = """Current date: 10/08/2023
    User: Long weekend trip next October. Can get either Friday or Monday off from work."""
    userExample_prompt3 = HumanMessagePromptTemplate.from_template(userExample3)

    botExample3 = """Answer: Long weekend usually means three days. Possible departure days are Thursday and Friday. Possible return flight days are Sunday or Monday. Outbound flight should be after work (assumed 6PM), return flight not too late for work next day.
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
    botExample_prompt3 = AIMessagePromptTemplate.from_template(botExample3)

    #example 4
    userExample4 = """Current date: 10/04/2023
    User: One-way trip to Paris in the summer."""
    userExample_prompt4 = HumanMessagePromptTemplate.from_template(userExample4)

    botExample4 = """Answer: The user only needs an outbound flight to Paris, which should be anytime in the summer months (June, July, August). Because it is a one-way trip, nights_in_dst-parameters must be excluded. 
    ```json
    {{
        "date_from": "01/06/2023",
        "date_to": "31/08/2023"
    }}
    ```"""
    botExample_prompt4 = AIMessagePromptTemplate.from_template(botExample4)

    #example 5
    userExample5 = """Current date: 10/07/2023
    User: Want to go abroad."""
    userExample_prompt5 = HumanMessagePromptTemplate.from_template(userExample5)

    botExample5 = """Answer: The user is very vague about when they want to go or for how long. To find two-way fligths we must include nights_in_dst-parameters, so we need to make assumptions. Let"s assume roughly one-week stay and look for flights in the next three months.
    ```json
    {{
        "date_from": "11/07/2023",
        "date_to": "10/10/2023",
        "nights_in_dst_from": 5,
        "nights_in_dst_to": 9
    }}
    ```"""
    botExample_prompt5 = AIMessagePromptTemplate.from_template(botExample5)


    human_template = """Current date: {current_date}
    User: {user_request}"""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt,
         userExample_prompt1,
         botExample_prompt1,
         userExample_prompt2,
         botExample_prompt2,
         userExample_prompt3,
         botExample_prompt3,
         userExample_prompt4,
         botExample_prompt5,
         userExample_prompt5,
         botExample_prompt5,
         human_message_prompt,]
    )

    #request the response from the model
    openai_response = chat(
        chat_prompt.format_prompt(
            user_request=user_request,
            current_date=current_date
        ).to_messages()
    )
    logger.info(str(openai_response.content))

    # Extract the json string using regular expressions
    import re
    import json
    json_str = re.search(r"\{.*\}", openai_response.content, re.DOTALL).group()

    # Convert the json string to a Python dictionary
    logger.info("json_str: %s", json_str)
    time_params = json.loads(json_str)
    time_params = adjust_dates(time_params) # Check if dates are in the past. If they are, add a year.
    logger.info("Time parameters created: %s", time_params)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"Function execution time: {elapsed_time} seconds")

    return time_params


# A helper function in case the dates are in the past
def adjust_dates(time_params):
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
        logging.warning('Both dates were in the past. Adjusted them to: %s - %s', time_params['date_from'], time_params['date_to'])

    return time_params

if __name__ == "__main__":
    test_request = "Origin: Helsinki, FI; Destination: Vilna; Departure: October, any Friday; Duration: 2 nights"
    print(create_time_params(test_request))