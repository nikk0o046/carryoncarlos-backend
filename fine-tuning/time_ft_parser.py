"""
This script is used to format the training data for the time parameters function to the format supported by OpenAI.
"""

import json

# Predefined system message.
system_template = """API DOCUMENTATION:
departure_date_from, departure_date_to: Range for outbound flight departure (dd/mm/yyyy). These must be included. If not provided, you must make an assumption.

nights_in_dst_from, nights_in_dst_to: Minimum and maximum stay length at the destination (in nights). Only exclude these if the user is looking for a one-way trip. If not provided, you must make an assumption.

fly_days, ret_fly_days: List of preferred days for outbound and return flights (0=Sunday, 1=Monday, ... 6=Saturday). 

fly_days_type, ret_fly_days_type: Specifies if fly_days/ret_fly_days is for an arrival or a departure flight.

If the user looks for specific dates, set departure_date_from and departure_date_to to a specific date, and match nights_in_dst_from and nights_in_dst_to so that the return day will be correct.

ANSWER INSTRUCTIONS:
Your task is to create parameters specified above based on user information. The parameters will be forwarded to another assistant, who uses them to search flights. Do not come up with any other parameters.
The output should include both:
1) Thought: Thinking out loud about the user's needs and the task.
2) Markdown code snippet formatted in the following schema, including the leading and trailing "\`\`\`json" and "\`\`\`":

```json
{
    "key1": value1  // Define relevant values. Only use keys mentioned in the API documentation. 
    "key2": value2
}
```"""

def generate_training_data(test_cases : list) -> list:
    """
    This function takes the test cases and generates the training data for the time parameters function.

    Args:
        test_cases (list): The test cases.

    Returns:
        list: The training data.
    """
    
    training_data = []

    for case in test_cases:
        date = case["date"]
        user_message_content = case["user_request"]
        formatted_user_message = f"Current date: {date}\nInfo: {user_message_content}"
        assistant_message_content = case["time_answer"]

        training_example = {
            "messages": [
                {"role": "system", "content": system_template},
                {"role": "user", "content": formatted_user_message},
                {"role": "assistant", "content": assistant_message_content}
            ]
        }
        training_data.append(training_example)

    return training_data
    

if __name__ == "__main__":
    # Load your test_cases from the JSON file.
    with open("../data/test_cases.json", "r") as file:
        test_cases = json.load(file)
        training_data = generate_training_data(test_cases)
    
    # Write the generated training data to a new JSONL file.
    with open("../data/time_training_data.jsonl", "w") as file:
        for example in training_data:
            file.write(json.dumps(example) + '\n')
            
    print("Training data generated and saved to time_training_data.jsonl.")