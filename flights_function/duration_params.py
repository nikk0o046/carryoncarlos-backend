import os
import re
import time
import logging
import json
logger = logging.getLogger(__name__)

from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate
)
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
# retrieve the OPENAI_API_KEY from environment variable
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

def create_duration_params(user_request, selectedCityID, user_id):
    start_time = time.time()
    logger.debug("[UserID: %s] Creating duration parameters...", user_id)

    # Initialize the openai model
    chat = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, openai_organization='org-aaoYoL6D18BG1Z1btni0f4i6', model="gpt-3.5-turbo")

    # Create the prompt templates
    system_template = """INSTRUCTIONS:
    You're an intelligent AI agent, and your job is to create search parameters about the flight duration, stopovers, and stopover duration.

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
    2) Markdown code snippet formatted in the following schema, including the leading and trailing "\`\`\`json" and "\`\`\`":

    ```json
    {{
        "key1": value1  // Define relevant values. Only use keys mentioned in the API documentation. 
        "key2": value2
    }}
    ```"""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

    #example 1
    userExample1 = """Origin: Madrid
    Info: Origin: Madrid, ES | Destination: Barcelona, ES | Departure: Next month | Duration: Weekend"""
    userExample_prompt1 = HumanMessagePromptTemplate.from_template(userExample1)

    botExample1 = """Thought: Considering the short-haul nature of Madrid to Barcelona and the short duration of the trip (weekend), direct flights would be ideal. Major hubs like Madrid and Barcelona have numerous direct flight options.
    ```json
    {{
        "max_sector_stopovers": 0
    }}
    ```"""
    
    botExample_prompt1 = AIMessagePromptTemplate.from_template(botExample1)

    #example 2
    userExample2 = """Origin: Helsinki
    Info: Origin: Helsinki, FI | Destination: South America | Departure: January | Duration: 2 weeks | Flights: Any"""
    userExample_prompt2 = HumanMessagePromptTemplate.from_template(userExample2)

    botExample2 = """Thought: The long-haul nature of Helsinki to South America, combined with the user's flexibility for any flights, suggests that we should allow some layovers. However, we'll aim to optimize for comfort by limiting lengthy stopovers and excessive travel time.
    ```json
    {{
        "max_fly_duration": 20,
        "max_sector_stopovers": 2
        "stopover_to": "5:00"
    }}
    ```"""
    botExample_prompt2 = AIMessagePromptTemplate.from_template(botExample2)

    #example 3
    userExample3 = """Origin: New York
    Info: "Origin: New York, US | Destination: Sydney, AU | Departure: March | Duration: 1 week | Flights: direct"""
    userExample_prompt3 = HumanMessagePromptTemplate.from_template(userExample3)

    botExample3 = """Thought: The user wants direct flights, so we set max_sector_stopovers to 0. We omit stopover_to and max_fly_duration for direct flights.
     ```json
    {{
        "max_sector_stopovers": 0
    }}
    ```"""
    botExample_prompt3 = AIMessagePromptTemplate.from_template(botExample3)

    human_template = """Origin: {selectedCityID}
    Info: {user_request}"""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt,
        userExample_prompt1,
        botExample_prompt1,
        userExample_prompt2,
        botExample_prompt2,
        userExample_prompt3,
        botExample_prompt3,
        human_message_prompt]
    )

    # Request the response from the model
    openai_response = chat(
        chat_prompt.format_prompt(
        selectedCityID=selectedCityID,
        user_request=user_request
        ).to_messages()
    )

    logger.debug("[UserID: %s] Duration parameters response: %s", user_id, openai_response.content)
    #print(openai_response.content) # FOR LOCAL TESTING 

    # Extract the json string using regular expressions
    json_str = re.search(r"\{.*\}", openai_response.content, re.DOTALL).group()
    
    # Convert the json string to a Python dictionary
    logger.debug("[UserID: %s] json_str: %s", user_id, json_str)
    duration_params = json.loads(json_str)
    logger.debug("[UserID: %s] Duration created: %s", user_id, duration_params)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.debug("[UserID: %s] Function execution time: %s seconds", user_id, elapsed_time)

    return duration_params


#test_request = "Origin: Helsinki, FI; Destination: Vilna; Departure: October, any Friday; Duration: 2 nights"
#print(create_duration_params(test_request, "Helsinki_fi", "test_id"))