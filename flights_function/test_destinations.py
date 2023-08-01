import os
import re

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

#initialize the openai model
chat = ChatOpenAI(temperature=0.5, openai_api_key = OPENAI_API_KEY)

user_request = "I want to go surfing"

#create the prompt templates
system_template = """INSTRUCTIONS:
You're an intelligent AI agent, and your job is to identify as many possible destination airports as you can based on the user's message. You will first think about the task, and then provide an exhaustive list of IATA airport codes that match the criteria. Always present these codes in a list format like [XXX,YYY,ZZZ]. In most cases, aim for at least 15 to 20 destinations. Including more options will increase the likelihood of finding the best flights for the user.

EXAMPLES:
User origin: Stockholm
User message: I want to travel somewhere in southern Europe that is by the Mediterranean.
Thought: The user wants to travel to southern Europe, specifically a location by the Mediterranean Sea. This includes countries like Spain, France, Italy, Malta, Slovenia, Croatia, Bosnia and Herzegovina, Montenegro, Albania, Greece, and Cyprus. I have included as many relevant airports as possible that have direct flights from Stockholm and are located near the Mediterranean Sea.
Destinations (IATA codes): [BCN,VLC,MRS,NCE,FCO,NAP,ATH,SKG,SPU,DBV,PMO,BOD,TLS,AHO,CAG,CTA,LCA,PFO,TIA,OLB,MLA,GRO]

User origin: Barcelona
User message: I want to go for a weekend getaway to a city in eastern Europe. I’d like to see some to a slightly less big city, so not just Budapest or Bucharest etc.
Thought: The user is interested in traveling to a less populated city in eastern Europe, excluding larger cities like Budapest or Bucharest. Thus, I've included an extensive list of smaller airports in Eastern Europe.
Destinations (IATA codes): [LWO,KIV,CLJ,GDN,BRQ,TSR,VAR,TAY,RJK,KSC,ODE,POZ,IEV,LVIV,SZZ,SOJ,VNO,KRK,SKP,TGD,SJJ,PRN,BEG]

User origin: Munich
User message: I need to get absolutely hammered in some cool nightclub.
Thought: The user is looking for a city renowned for its nightlife. Cities known for their nightclubs and party scenes are numerous. So, I've included a wide range of potential locations.
Destinations (IATA codes): [IBZ,BCN,AMS,PRG,BUD,LIS,DUB,SPU,KRK,CDG,BER,LON,CPH,ROM,MAD,RIX,TLL,HEL,OSL,SOF,ZAG,BEG]

User origin: Paris
User message: I want to go to Amsterdam for a week in the summer.
Thought: The user has a specific destination in mind: Amsterdam. Therefore, the only relevant destination airport code is that of Amsterdam.
Destinations (IATA codes): [AMS]

User origin: Sydney
User message: I just want to get out of here, I don't care where.
Thought: The user is looking to travel, but hasn't specified a particular destination. Therefore, I've considered popular and accessible destinations from Sydney. The list includes a diverse range of domestic and international locations to offer the user an extensive array of choices.
Possible destinations (IATA codes): [MEL,BNE,ADL,PER,CBR,OOL,AKL,CHC,WLG,ZQN,NAN,DPS,SIN,KUL,BKK,HKT,HKG,TPE,NRT,HND,ICN,PEK,PVG,SFO,LAX,YVR,HNL,JFK,LHR,DXB,DOH]
"""
system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
human_template = """User origin: Helsinki
User message: {user_request}
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

print(openai_response.content)

# Regular expression pattern to match the IATA codes
pattern = r'\[([A-Za-z,\s]+)\]'

# Find the matches in the response content
matches = re.search(pattern, openai_response.content)

# If a match was found
if matches:
    # Get the matched string, remove spaces, and split it into a list on the commas
    destination_list = matches.group(1).replace(" ", "").split(',')

    # Create a destination dictionary from the response
    destination_params = {
        'fly_to' : ','.join(destination_list),
    }

    # Print the destination parameters
    print(destination_params)
else:
    print("No destinations found in the response.")

