import os
import openai

# Load the environment variables
from dotenv import load_dotenv
load_dotenv()

# Set up the OpenAI API key and organization ID from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_destination_airports(origin, destination_hint):
    # Define the prompt template
    prompt_template = f"""
    You are an advanced AI trained to provide IATA airport codes based on travel preferences. Given the origin '{origin}' and the destination hint '{destination_hint}', list suitable destination airports.
    """

    # Make the API call
    response = openai.Completion.create(
      model="ft-gpt-3.5-turbo-0613:personal::7sEp8ziH", # Your fine-tuned model name
      prompt=prompt_template,
      temperature=0,
      max_tokens=150
    )

    # Extract the response content
    response_content = response.choices[0].text.strip()

    return response_content

# Example usage of the function
origin = "Stockholm"
destination_hint = "southern Europe, by the Mediterranean"
print(get_destination_airports(origin, destination_hint))
