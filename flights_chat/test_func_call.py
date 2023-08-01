import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

import logging
logging.basicConfig(level=logging.INFO)

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
# retrieve the OPENAI_API_KEY from environment variable
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

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

app = Flask(__name__)
CORS(app)

@app.route('/send_message', methods=['POST'])
def send_message():
    # Get the request data
    request_data = request.get_json()

    # Extract the conversation history
    conversation_history = request_data.get('conversationHistory', [])

    # Pass the conversation history to your conversation handling function
    result = handle_conversation(conversation_history)

    # At the end, return a response
    return jsonify({"status": "success", "message": result})


def handle_conversation(conversation_history):
    message_list = [{"role": "system", "content": system_template}]
    message_list.extend(conversation_history)

    completion = openai.ChatCompletion.create(
        temperature = 0.5, 
        model = "gpt-3.5-turbo-0613", 
        api_key = OPENAI_API_KEY, 
        messages = message_list,
        functions = [json_schema]
    )

    message_content = completion.choices[0].message
    message_list.append(message_content)

    logging.info("Message: %s", message_content)
    logging.info("Function call in message: %s", 'function_call' in message_content)

    return message_list


