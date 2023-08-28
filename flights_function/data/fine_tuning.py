import os
import openai
from dotenv import load_dotenv, find_dotenv

# Load .env file
load_dotenv(find_dotenv())

# Setup API Key and Configuration
openai.api_key = os.getenv("OPENAI_API_KEY")
"""
# Set the paths for your files
train_data_path = "dest_training_data.jsonl"
validation_data_path = "dest_validation_data.jsonl"

# Upload Data Files
train_file = openai.File.create(
    file=open(train_data_path, "rb"),
    purpose='fine-tune'
)
print(f"Train file uploaded with ID: {train_file.id}")

validation_file = openai.File.create(
    file=open(validation_data_path, "rb"),
    purpose='fine-tune'
)
print(f"Validation file uploaded with ID: {validation_file.id}")

# Create Fine-Tuning Job
fine_tuning_job = openai.FineTuningJob.create(
    training_file="file-LFKbP9pO0l0X6OKp0lUh88MQ", 
    validation_file="file-t3NFtWM1tdpFg56XMouCjiWS",
    model="gpt-3.5-turbo"
)
"""

# Print fine-tuning job details
#print(f"Fine-tuning job created with ID: {fine_tuning_job.id}")
#Fine-tuning job created with ID: ftjob-3OL813BVj8tLQcFLxz4fLjAz

# Retrieve the state of a fine-tune
print(openai.FineTuningJob.retrieve("ftjob-3OL813BVj8tLQcFLxz4fLjAz"))
# List up to 10 events from a fine-tuning job
print(openai.FineTuningJob.list_events(id="ftjob-3OL813BVj8tLQcFLxz4fLjAz", limit=10))
#ft:gpt-3.5-turbo-0613:personal::7sEp8ziH