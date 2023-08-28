import json

# Your predefined system message.
system_template = """You are an advanced AI agent tasked with identifying as many potential destination airports as possible based on user preferences. Your response should include:

1. An initial thought process or reasoning for the task.
2. An exhaustive list of IATA airport codes matching the criteria, formatted as [XXX,YYY,ZZZ].

For ambiguous destinations, aim for at least 15 to 20 airport codes. Offering more options increases the chances of finding affordable flights for the user. Focus on final destination airports only, excluding connecting airports. Disregard any irrelevant information.
"""

def generate_training_data(test_cases):
    training_data = []

    for case in test_cases:
        user_message_content = case["user_request"]
        assistant_message_content = case["destination_answer"]

        training_example = {
            "messages": [
                {"role": "system", "content": system_template},
                {"role": "user", "content": user_message_content},
                {"role": "assistant", "content": assistant_message_content}
            ]
        }
        training_data.append(training_example)

    return training_data

if __name__ == "__main__":
    # Load your test_cases from the JSON file.
    with open("test_cases.json", "r") as file:
        test_cases = json.load(file)
        training_data = generate_training_data(test_cases)
    
    # Write the generated training data to a new JSONL file.
    with open("dest_training_data.jsonl", "w") as file:
        for example in training_data:
            file.write(json.dumps(example) + '\n')
            
    print("Training data generated and saved to training_data.jsonl.")
