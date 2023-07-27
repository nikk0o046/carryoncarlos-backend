import os
from datetime import datetime
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
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def create_time_params(user_request):
    logger.info("Creating time parameters...")
    current_date_unformatted = datetime.now()
    current_date = f"{current_date_unformatted:%d/%m/%Y}"

    #initialize the openai model
    chat = ChatOpenAI(temperature=0, openai_api_key = OPENAI_API_KEY, openai_organization="org-aaoYoL6D18BG1Z1btni0f4i6", model="gpt-4")

    #create the prompt templates
    system_template = """API DOCUMENTATION:
    date_from, date_to: Range for outbound flight departure (dd/mm/yyyy). 

    nights_in_dst_from, nights_in_dst_to: Minimum and maximum stay length at the destination (in nights). Only exclude these if the user is looking for a one-way trip. Otherwise you must make an assumption.

    fly_days, ret_fly_days: List of preferred days for outbound and return flights (0=Sunday, 1=Monday, ... 6=Saturday). 

    fly_days_type, ret_fly_days_type: Specifies if fly_days/ret_fly_days is for an arrival or a departure flight. 

    dtime_from, dtime_to, ret_dtime_from, ret_dtime_to: Define the earliest and latest departure time for outbound and return flights. 

    atime_from, atime_to, ret_atime_from, ret_atime_to: Define the earliest and latest arrival time for outbound and return flights.


    EXAMPLES:
    Current date: 10/07/2023
    User: "Weekend getaway in Paris next month. Off work on Friday around 3pm."
    Answer: User wants to leave on a Friday next month and stay for two nights. Outbound flight should be after work (assumed 5PM), return flight should not be too late for work next day.
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
        "ret_dtime_to": "18:00",
    }}
    ```

    Current date: 01/01/2024
    User: "On vacation next March. Want to go abroad for about a week."
    Answer: The trip can be done within the vacation dates next March, lasting about a week.
    ```json
    {{
    "date_from": "01/03/2024",
    "date_to": "31/03/2024",
    "nights_in_dst_from": 6,
    "nights_in_dst_to": 8,
    }}
    ```

    Current date: 10/08/2023
    User: "Long weekend trip next October. Can get either Friday or Monday off from work."
    Answer: Long weekend usually means three days. Possible travel days are Thursday, Friday, Saturday, Sunday, or Monday. Outbound flight should be after work (assumed 6PM), return flight not too late for work next day.
    ```json


    {{
        "date_from": "01/10/2023",
        "date_to": "31/10/2023",
        "nights_in_dst_from": 3,
        "nights_in_dst_to": 3,
        "fly_days": [4, 5],
        "dtime_from": "18:00",
        "ret_fly_days": [0, 1],
        "ret_dtime_to": "20:00",
    }}
    ```

    Current date: 10/04/2023
    User: "One-way trip to Paris in the summer."
    Answer: The user only needs an outbound flight to Paris, which should be anytime in the summer months (June, July, August). Because it is a one-way trip, nights_in_dst-parameters must be excluded. 
    ```json
    {{
        "date_from": "01/06/2023",
        "date_to": "31/08/2023",
    }}
    ```

    Current date: 10/07/2023
    User: "Want to go abroad."
    Answer: The user is very vague about when they want to go or for how long. To find two-way fligths we must include nights_in_dst-parameters, so we need to make assumptions. Let"s assume roughly one-week stay and look for flights in the next three months.
    ```json
    {{
        "date_from": "11/07/2023",
        "date_to": "10/10/2023",
        "nights_in_dst_from": 5,
        "nights_in_dst_to": 9,
    }}
    ```

    ANSWER INSTRUCTIONS:
    The output should include both:
    1) Thought: Thinking out loud about the user"s needs and the task.
    2) Markdown code snippet formatted in the following schema, including the leading and trailing "\`\`\`json" and "\`\`\`":

    ```json
    {{
        "key1": value1  // Define relevant values  
        "key2": value2 
    }}
    ``` """

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Current date: {current_date}
    User: {user_request}
    Answer: """
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
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
    time_params = json.loads(json_str)
    logger.info("Time parameters created: %s", time_params)

    return time_params
