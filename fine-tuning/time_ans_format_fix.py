import json

# Read the file containing response content
with open('../data/time_answers_raw.json', 'r') as file:
    file_content = file.read().strip()

# Split the content into individual JSON strings and remove empty strings
json_strings = [s for s in file_content.split('\n') if s]

# Parse each string into a dictionary and add to a list
response_data = [json.loads(json_string) for json_string in json_strings]

# Read the original JSON with test case details
with open('../data/test_cases.json', 'r') as file:
    original_data = json.load(file)

# Create a mapping from test_case_number to date and user_request
test_case_mapping = {item['test_case_number']: {'date': item['date'], 'user_request': item['user_request']}
                     for item in original_data}

# Merge the data and rearrange the order
merged_data = []
for item in response_data:
    test_case_number = item.get('test_case_number')
    if test_case_number in test_case_mapping:
        new_item = test_case_mapping[test_case_number]  # Start with date and user_request
        new_item.update(item)  # Add the rest of the keys
        merged_data.append(new_item)

# Write the merged data to the formatted output file
with open('../data/time_answers_raw_formatted.json', 'w') as outfile:
    json.dump(merged_data, outfile, indent=4)
