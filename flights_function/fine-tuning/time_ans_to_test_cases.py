import json

# Load the answers
with open("../data/time_answers_edited.json", "r") as file:
    answers = json.load(file)

# Load the test cases
with open("../data/test_cases.json", "r") as file:
    test_cases = json.load(file)

# Append the answers to the test cases
for i, test_case in enumerate(test_cases):
    answer = answers[i]["response_content"]
    test_case["time_answer"] = answer

# Write the updated test cases back to the file
with open("../data/test_cases.json", "w") as file:
    json.dump(test_cases, file, indent=4)