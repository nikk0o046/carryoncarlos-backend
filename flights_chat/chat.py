import os
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

import logging
#from google.cloud import logging as cloudlogging
#client = cloudlogging.Client()
#client.setup_logging(log_level=logging.DEBUG) 
#logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

You need to get the following information about the user:
- The city they want to travel from and a description of a location they want to travel to. It is okay if that is a bit vague, like “somewhere warm in Europe”.
- Time window when they can departure and approximately how many days they want to stay.
- Does the user prefer direct flights or are layovers ok.
Try to ask one question at a time.

When (and only when) you have the necessary information, call search_flights -function with one string parameter. The string is your concise summary about the relevant user information."""

app = Flask(__name__)
CORS(app)

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        user_id = request.headers.get('Customer-ID', 'Not Provided')

        # Log the raw incoming request data
        logger.debug("[User: %s] Raw request data: %s", user_id, request.data)

        # Get the request data
        request_data = request.get_json()

        # Extract the conversation history
        conversation_history = request_data.get('conversationHistory', [])

        # Log the conversation history
        logger.info("[User: %s] Conversation history: %s", user_id, conversation_history)

        # Pass the conversation history to your conversation handling function
        result = handle_conversation(conversation_history, user_id)

        # At the end, return a success response
        return jsonify({"status": "success", "message": result}), 200

    except Exception as e:
        # Log the error
        logger.error("[User: %s] An error occurred: %s", user_id, str(e))
        
        # Return an error response
        return jsonify({"status": "error", "message": "An error occurred."}), 500


def handle_conversation(conversation_history, user_id):
    message_list = [{"role": "system", "content": system_template}]
    message_list.extend(conversation_history)

    # Check if the third message is the user's and if it contains the 'user_inputs' key
    if 'user_inputs' in message_list[2]:
        user_data = message_list[2]['user_inputs']
        originCity = user_data['originCity']
        travelers = user_data['travelers']

        formatted_content = f"User origin city: {originCity}. Travelling: {travelers['adults']} adults, {travelers['children']} children, {travelers['infants']} infants. {message_list[2]['content']}"

        # Modify the user's message content
        message_list[2]['content'] = formatted_content

        # Remove the 'data' key as it's no longer needed
        del message_list[2]['user_inputs']

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
    logger.debug("[User: %s] Time taken for OpenAI API request: %s seconds", user_id, elapsed_time)

    new_message = completion.choices[0].message

    logger.info("[User: %s] Message: %s", user_id, new_message)
    logger.debug("[User: %s] Function call in message: %s", user_id, 'function_call' in new_message)

    return new_message


# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8081))
    app.run(host='0.0.0.0', port=port)
