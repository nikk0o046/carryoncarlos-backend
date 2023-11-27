"""
This script by OpenAI is used to fine-tune the model. It is important to make sure that the data is formatted correctly before training the model.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

# Load .env file
load_dotenv(find_dotenv())

# Setup API Key and Configuration
OpenAI.api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

# Set the paths for your files
train_data_path = "../data/time_training_data.jsonl"
validation_data_path = "../data/time_validation_data.jsonl"

# Upload Data Files
train_file = client.files.create(
    file=open(train_data_path, "rb"),
    purpose='fine-tune'
)
print(f"Train file uploaded with ID: {train_file.id}")

validation_file = client.files.create(
    file=open(validation_data_path, "rb"),
    purpose='fine-tune'
)
print(f"Validation file uploaded with ID: {validation_file.id}")

# Create Fine-Tuning Job
fine_tuning_job = client.fine_tuning.jobs.create(
    training_file="file-MxdpqYwSSa1Q8d3ex7AusaY2", 
    validation_file="file-XE9ez3CetCAmFxH6EjZvahhp",
    model="gpt-3.5-turbo"
)

# Print fine-tuning job details
print(f"Fine-tuning job created with ID: {fine_tuning_job.id}")

# Retrieve the state of a fine-tune
print(client.fine_tuning.jobs.retrieve("ftjob-l4HKvwvQgn7O8EvCJbSxUx1x"))
# List up to 10 events from a fine-tuning job
print(client.fine_tuning.jobs.list_events(fine_tuning_job_id="ftjob-l4HKvwvQgn7O8EvCJbSxUx1x", limit=10))
