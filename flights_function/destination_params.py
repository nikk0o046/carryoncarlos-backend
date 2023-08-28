import os
import re
import time
import logging
logger = logging.getLogger(__name__)
import openai

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
# retrieve the OPENAI_API_KEY from environment variable
openai.api_key = os.environ.get('OPENAI_API_KEY')
openai.organization = os.environ.get('OPENAI_ORG_ID')

def create_destination_params(user_request, selectedCityID, user_id):
    start_time = time.time() #start timer to log it later
    logger.debug("[UserID: %s] Creating destination parameters...", user_id)

    #create the prompt templates
    system_template1 = """INSTRUCTIONS:
    You're an intelligent AI agent, and your job is to identify as many possible destination airports as you can based on information provided about the user preferences.
    You will first think about the task, and then provide an exhaustive list of IATA airport codes that match the criteria. Always present these codes in a list format like [XXX,YYY,ZZZ].
    When destination is not one specific place, usually aim for at least 15 to 20 destinations. Including more options will increase the likelihood of finding cheap flights for the user.
    Only include final destination airports, not origin or layover. No duplicates codes."""
    
    system_template = """You are an advanced AI agent tasked with identifying as many potential destination airports as possible based on user preferences. Your response should include:

1. An initial thought process or reasoning for the task.
2. An exhaustive list of IATA airport codes matching the criteria, formatted as [XXX,YYY,ZZZ].

For ambiguous destinations, aim for at least 15 to 20 airport codes. Offering more options increases the chances of finding affordable flights for the user. Focus on final destination airports only, excluding connecting airports. Disregard any irrelevant information."""

    #example 1
    userExample1 = """Origin: Stockholm
    Info: Origin: Stockholm, SE | Destination: southern Europe, by the Mediterranean | Departure: Flexible | Duration: 3 nights | Flights: direct"""

    botExample1 = """Thought: The user wants to travel to southern Europe, specifically a location by the Mediterranean Sea. This includes countries like Spain, France, Italy, Malta, Slovenia, Croatia, Bosnia and Herzegovina, Montenegro, Albania, Greece, and Cyprus. I have included as many relevant airports as possible that have direct flights from Stockholm and are located near the Mediterranean Sea.
    Destinations (IATA codes): [BCN,VLC,MRS,NCE,FCO,NAP,ATH,SKG,SPU,DBV,PMO,BOD,TLS,AHO,CAG,CTA,LCA,PFO,TIA,OLB,MLA,GRO]"""

    #example 2
    userExample2 = """Origin: Barcelona
    Info: Origin: Barcelona, ES | Destination: eastern Europe, smaller city | Departure: Weekend | Duration: 2-3 days | Flights: Any"""

    botExample2 = """Thought: The user is interested in traveling to a less populated city in eastern Europe, excluding larger cities like Budapest or Bucharest. Thus, I've included an extensive list of smaller airports in Eastern Europe.
    Destinations (IATA codes): [LWO,KIV,CLJ,GDN,BRQ,TSR,VAR,TAY,RJK,KSC,ODE,POZ,IEV,LVIV,SZZ,SOJ,VNO,KRK,SKP,TGD,SJJ,PRN,BEG]"""

    #example 3
    userExample3 = """Origin: Munich
    Info: Origin: Munich, DE | Destination: Any | Activity: Nightlife | Departure: May | Duration: 4-5 nights | Flights: Any"""

    botExample3 = """Thought: The user is looking for a city renowned for its nightlife. Cities known for their nightclubs and party scenes are numerous. So, I've included a wide range of potential locations.
    Destinations (IATA codes): [IBZ,BCN,AMS,PRG,BUD,LIS,DUB,SPU,KRK,CDG,BER,LON,CPH,ROM,MAD,RIX,TLL,HEL,OSL,SOF,ZAG,BEG]"""

    #example 4
    userExample4 = """Origin: Paris
    Info: Origin: Paris, FR | Destination: Amsterdam | Departure: Summer | Duration: 1 week | Flights: Any"""

    botExample4 = """Thought: The user has a specific destination in mind: Amsterdam. Therefore, the only relevant destination airport code is that of Amsterdam.
    Destinations (IATA codes): [AMS]"""

    #example 5
    userExample5 = """Origin: Sydney
    Info: Origin: Sydney, AU | Destination: Any | Departure: Flexible | Duration: Flexible | Flights: Any"""

    botExample5 = """Thought: The user is looking to travel, but hasn't specified a particular destination. Therefore, I've considered popular and accessible destinations from Sydney. The list includes a diverse range of domestic and international locations to offer the user an extensive array of choices.
    Possible destinations (IATA codes): [MEL,BNE,ADL,PER,CBR,OOL,AKL,CHC,WLG,ZQN,NAN,DPS,SIN,KUL,BKK,HKT,HKG,TPE,NRT,HND,ICN,PEK,PVG,SFO,LAX,YVR,HNL,JFK,LHR,DXB,DOH]"""

    #human_template = f"Origin: {selectedCityID}\nInfo: {user_request}"
    human_template = user_request

    # Construct the conversation message list
    message_list = [
        {"role": "system", "content": system_template},
        #{"role": "user", "content": userExample1},
        #{"role": "assistant", "content": botExample1},
        #{"role": "user", "content": userExample2},
        #{"role": "assistant", "content": botExample2},
        #{"role": "user", "content": userExample3},
        #{"role": "assistant", "content": botExample3},
        #{"role": "user", "content": userExample4},
        #{"role": "assistant", "content": botExample4},
        #{"role": "user", "content": userExample5},
        #{"role": "assistant", "content": botExample5},
        {"role": "user", "content": human_template}
    ]

    # Request the response from the model
    response = openai.ChatCompletion.create(
      #model="gpt-3.5-turbo-0613",
      model="ft:gpt-3.5-turbo-0613:personal::7sEp8ziH",
      temperature=0,
      messages=message_list,
    )
    response_content = response.choices[0].message['content']

    logger.debug("[UserID: %s] Destination parameters response: %s", user_id, response_content)
    
    print("response_content: " + str(response_content)) # FOR LOCAL TESTING
    print("Prompt Tokens Used: " + str(response["usage"]['prompt_tokens']) + " | Completion Tokens Used: " + str(response["usage"]['completion_tokens']) + " | Total Tokens Used: " + str(response["usage"]['total_tokens']))

    # Regular expression pattern to match the IATA codes
    pattern = r'\[([A-Za-z,\s]+)\]'

    # Find the matches in the response content
    matches = re.search(pattern, response_content)

    # If a match was found
    if matches:
        # Get the matched string, remove spaces, and split it into a list on the commas
        destination_list = matches.group(1).replace(" ", "").split(',')

        # Create a destination dictionary from the response
        destination_params = {
            'fly_to' : ','.join(destination_list),
        }

    else:
        destination_params = {}

    logger.debug("[UserID: %s] Destination parameters created: %s", user_id, destination_params)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.debug("[UserID: %s] Function execution time: %s seconds", user_id, elapsed_time)

    return destination_params

#test_request = "Origin: Helsinki, FI; Destination: Vilna; Departure: October, any Friday; Duration: 2 nights"
test_request = "Origin: Helsinki | Destination: Polynesia | Departure: End of September | Duration: 7 days | Flights: Any"
print(create_destination_params(test_request, "Helsinki_fi", "test_id"))
