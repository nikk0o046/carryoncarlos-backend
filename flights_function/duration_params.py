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
    You're an intelligent AI agent, and your job is to create smart search parameters about the flight duration, stopovers, and stopover duration.

    INSTRUCTIONS:
    Create search parameters for flights based on user input. If the user does not specify those specifically, use your reasoning abilities to define relevant values.

    max_sector_stopovers: max number of stopovers per itinerary's sector (integer).
    stopover_to: max length of stopover, 4:00 means 4 hours. Usually keep this under 5:00.
    max_fly_duration: max itinerary duration in hours (integer), from start of the departure to the arrival, including stopovers. Usually keep this under 20.
    
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
    userExample1 = """Origin: Madrid
    User: User wants to go to Barcelona for a weekend trip some time in the next month"""
    userExample_prompt1 = HumanMessagePromptTemplate.from_template(userExample1)

    botExample1 = """Thought: The user want to travel from Madrid to Barcelona. The cities have many direct connections and the user is looking for a weekend trip so we should set max_sector_stopovers to 0. As there are no stopovers, we omit max_stopover parameter. Also we omit max_fly_duration, as all direct flights tend to be pretty similar in the amount of time they take.
    ```json
    {{
        "max_sector_stopovers": 0
    }}
    ```"""
    
    botExample_prompt1 = AIMessagePromptTemplate.from_template(botExample1)

    #example 2
    userExample2 = """Origin: Helsinki
    User: User wants to go to South America for two weeks in January."""
    userExample_prompt2 = HumanMessagePromptTemplate.from_template(userExample2)

    botExample2 = """Thought: The user is traveling very far away, for a long time and is flexible with the destination. We set max_sector_stopovers to 2 to allow for much flexibility. We set stopover_to to 5 hours to allow for connections with a quite lenghty gap. We set max_fly duration to 20 hours to filter out routes that take way too long.
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
    User: User wants directs flights to Sydney in March for a week."""
    userExample_prompt3 = HumanMessagePromptTemplate.from_template(userExample3)

    botExample3 = """Thought: The user specifically says that they want direct flights, so we set max_sector_stopovers to 0. As there are no stopovers, we omit max_stopover parameter. Also we omit max_fly_duration, as all direct flights tend to be pretty similar in the amount of time they take.
     ```json
    {{
        "max_sector_stopovers": 0
    }}
    ```"""
    botExample_prompt3 = AIMessagePromptTemplate.from_template(botExample3)

    human_template = """Origin: {selectedCityID}
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
        human_message_prompt]
    )

    # Request the response from the model
    openai_response = chat(
        chat_prompt.format_prompt(
        selectedCityID=selectedCityID,
        user_request=user_request
        ).to_messages()
    )

    print(openai_response.content)
    logger.debug("[UserID: %s] Duration parameters response: %s", user_id, openai_response.content)

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

#if __name__ == "__main__":
    #test_request = "Origin: Helsinki, FI; Destination: Vilna; Departure: October, any Friday; Duration: 2 nights"
    #print(create_duration_params(test_request, "Helsinki_fi"))