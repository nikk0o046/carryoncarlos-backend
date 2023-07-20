import os
import logging
logger = logging.getLogger(__name__)

from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
# retrieve the OPENAI_API_KEY from environment variable
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

def create_destination_params(user_request):
    logger.info("\nCreating destination parameters...")

    #initialize the openai model
    chat = ChatOpenAI(temperature=0, openai_api_key = OPENAI_API_KEY)

    #create the prompt templates
    system_template = """/
    User origin: Stockholm
    User message: I want to travel somewhere in southern Europe that is by Mediterranean.
    Possible destinations (IATA codes): [BCN,VLC,MRS,NCE,FCO,NAP,ATH,SKG,SPU,SBV]
    ---
    User origin: Barcelona
    User message: I want to go for a weekend getaway to a city in eastern Europe. I’d like to see some to a slightly less big city, so not just Budapest or Bucharest etc.
    Possible destinations (IATA codes): [LWO,KIV,CLJ,GDN,BRQ,TSR,VAR,TAY,RJK,KSC]
    ---
    User origin: Munich
    User message: I need to get absolutely hammered in some cool nightclub.
    Possible destinations (IATA codes): [IBZ,BCN,AMS,PRG,BUD,LIS,DUB,SPU,KRK,CDG]
    ---
    User origin: Paris
    User message: I want to go to Amsterdam for a week in the summer.
    Possible destinations (IATA codes): [AMS]
    ---
    User origin: Helsinki
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """User message: {user_request}
    Possible destinations (IATA codes): """
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

    # Remove the brackets and spaces, then split the string into a list on the commas
    destination_list = openai_response.content.replace("[", "").replace("]", "").replace(" ", "").split(",")

    # Now you should be able to join the list into a single string with commas
    destination_string = ",".join(destination_list)

    # Create a destination dictionary from the response
    destination_params = {
        'fly_to' : destination_string,
    }

    logger.info("Destination parameters created: %s", destination_params)
    return destination_params

#logger.info(create_destination_params("I want to go to London in September 2023 during the weekend."))
