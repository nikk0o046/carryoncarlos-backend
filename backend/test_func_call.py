import os
import pprint
import openai
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
# retrieve the OPENAI_API_KEY from environment variable
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

import requests
import json

def send_request_to_flask_app(summary_info):
    url = "http://localhost:8080/search_flights"  # Replace with your Flask app's URL
    headers = {'Content-type': 'application/json'}
    data = json.dumps({"user_request": summary_info})

    response = requests.post(url, data=data, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None
    
json_schema = {
    "name": "search_flights",
    "description": "Search flights based on summary of user information",
    "parameters": {
        "type": "object",
        "properties": {
            "summary_info": {
                "type": "string", 
                "description": "Description of flights the user is looking for."
            },
        },
        "required": ["summary_info"],
    }
}


system_template = """You are a flight search assistant named Carry-on Carlos. You need to gather some information about the user, so you can make a request for a flight search assistant to get flights for them. Your description is below: 

Carlos is a well-traveled, charming suitcase who’s seen the inside of all the world's airports.
Behaviour Type: Carlos is knowledgeable, occasionally grumpy, and loves to complain about rough baggage handlers.
Other facts: He has a scar from a customs incident in 2019, and is slightly afraid of conveyor belts.

You need to get the following information about the user:
- The city they want to travel from and a description of a location they want to travel to. It is okay if that is a bit vague, like “somewhere warm in Europe”.
- Time window when they can departure and approximately how many nights they want to stay.
Try to ask one question at a time.

When you have the necessary information, call search_flights -function with one string parameter. The string is your concise summary about the relevant user information."""

botMessage1 = """Hello there, fellow traveler! This is your Carry-on Carlos speaking. I've weathered more baggage carousels and customs checkpoints than you've had hot dinners, so you can trust I'm good at finding the right flight for you! To get us started, please tell me the city you're taking off from and give me a description of where you want to land."""
print(botMessage1)

message_list = []
message_list.append({"role": "system", "content": system_template})
message_list.append({"role": "assistant", "content": botMessage1})


for i in range(10):
    user_input = input("Write your message here: ")
    message_list.append({"role": "user", "content": user_input})

    completion = openai.ChatCompletion.create(
        temperature = 0.5, 
        model = "gpt-3.5-turbo-0613", 
        api_key = OPENAI_API_KEY, 
        messages = message_list,
        functions = [json_schema]
    )
    message = completion.choices[0].message
    message_list.append(message)
    print(message)
    print('function_call' in message)

    if ('function_call' in message):
        print("executing if block")
        step1 = message['function_call']
        print(step1)
        step2 = step1['arguments']
        print(step2)
        print(type(step2))
        arguments_dict = json.loads(step2)
        summary_info = arguments_dict['summary_info']
        print(summary_info)
        #summary_info = message['function_call']['arguments']['summary_info']  # Now you can index it with ['summary_info']
        flight_results = send_request_to_flask_app(summary_info)
        if flight_results:
            for flight in flight_results:
                pprint.pprint(flight)
        else:
            print("No flights found or there was an error.")


