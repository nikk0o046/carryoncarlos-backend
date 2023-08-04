import os
import time
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

When (and only when) you have the necessary information, call search_flights -function with one string parameter. The string is your concise summary about the relevant user information."""

app = Flask(__name__)
CORS(app)

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        # Log the raw incoming request data
        logging.info("Raw request data: %s", request.data)

        # Get the request data
        request_data = request.get_json()

        # Extract the conversation history
        conversation_history = request_data.get('conversationHistory', [])

        # Log the conversation history
        logging.info("Conversation history: %s", conversation_history)

        # Pass the conversation history to your conversation handling function
        result = handle_conversation(conversation_history)

        # At the end, return a success response
        return jsonify({"status": "success", "message": result}), 200

    except Exception as e:
        # Log the error
        logging.error("An error occurred: %s", str(e))
        
        # Return an error response
        return jsonify({"status": "error", "message": "An error occurred."}), 500


def handle_conversation(conversation_history):
    message_list = [{"role": "system", "content": system_template}]
    message_list.extend(conversation_history)

    start_time = time.time()  # Get the current time to see OpenAI response time
    completion = openai.ChatCompletion.create(
        temperature = 0.5, 
        model = "gpt-3.5-turbo-0613", 
        api_key = OPENAI_API_KEY, 
        messages = message_list,
        functions = [json_schema]
    )
    end_time = time.time()  # Get the current time again after the request is made
    elapsed_time = end_time - start_time  # Calculate the difference
    logging.info("Time taken for OpenAI API request: %s seconds", elapsed_time)

    new_message = completion.choices[0].message

    logging.info("Message: %s", new_message)
    logging.info("Function call in message: %s", 'function_call' in new_message)

    return new_message


# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8081))
    app.run(host='0.0.0.0', port=port)
