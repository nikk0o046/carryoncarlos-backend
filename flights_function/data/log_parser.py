from google.cloud import logging
from google.cloud.logging import DESCENDING
import re
import json

def capture_user_data():
    """Captures and aggregates user-related information from the logs."""
    
    # Initialize the logging client
    logging_client = logging.Client()
    
    # Initialize an empty dictionary to store user data
    user_data = {}
    
    # Query filter
    query_filter = 'severity>="DEBUG"'  # This should capture DEBUG, INFO, and higher
    
    log_counter = 0  # To keep track of how many logs were processed

    # Loop through each log entry
    for entry in logging_client.list_entries(order_by=DESCENDING, filter_=query_filter):
        log_counter += 1  # Increment the log counter
        
        # Extract the text payload from the log entry
        text_payload = entry.payload
        
        # Regular expression to capture the user ID and the associated message
        match = re.search(r"\[UserID: (.+?)\] (.+)", text_payload)
        
        if match:
            user_id, message = match.groups()

            # Initialize a dictionary for this user ID if it doesn't exist
            if user_id not in user_data:
                user_data[user_id] = {}
                print(f"Added User ID: {user_id}")  # Print when a new User ID is added

            # Further parsing logic to capture different types of data
            # Capture "key: value" pairs
            key_value_match = re.search(r"(\w+): (.+)", message)
            if key_value_match:
                key, value = key_value_match.groups()

                # Special handling for 'travelers' as it is a JSON-like string
                if key == 'travelers':
                    value = value.replace("'", '"')  # replace single quotes with double quotes
                    value = json.loads(value)  # convert the JSON-like string to a Python dictionary
                
                user_data[user_id][key] = value

    print(f"Processed {log_counter} log entries.")
    print(f"Captured user data: {user_data}")
    
    return user_data

# Execute the function
captured_data = capture_user_data()
