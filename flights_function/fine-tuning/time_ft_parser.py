from dest_ft_parser import generate_training_data
import json

# Predefined system message.
system_template = """xxx
"""
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