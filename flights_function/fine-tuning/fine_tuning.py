import os
import openai
from dotenv import load_dotenv, find_dotenv

# Load .env file
load_dotenv(find_dotenv())

# Setup API Key and Configuration
openai.api_key = os.getenv("OPENAI_API_KEY")
"""
# Set the paths for your files
train_data_path = "./data/dest_training_data.jsonl"
validation_data_path = "./data/dest_validation_data.jsonl"

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
    training_file="file-eHq7uKNF4cihXKmj5IIbGHgl", 
    validation_file="file-BocazJt8vBa4rtHRGWroIuvW",
    model="gpt-3.5-turbo"
)

# Print fine-tuning job details
print(f"Fine-tuning job created with ID: {fine_tuning_job.id}")
#Fine-tuning job created with ID: ftjob-xhaP1dDASdwldTCUoMYllWUi
"""

# Retrieve the state of a fine-tune
print(openai.FineTuningJob.retrieve("ftjob-xhaP1dDASdwldTCUoMYllWUi"))
# List up to 10 events from a fine-tuning job
print(openai.FineTuningJob.list_events(id="ftjob-xhaP1dDASdwldTCUoMYllWUi", limit=10))
"""
{
  "object": "fine_tuning.job",
  "id": "ftjob-xhaP1dDASdwldTCUoMYllWUi",
  "model": "gpt-3.5-turbo-0613",
  "created_at": 1699091401,
  "finished_at": null,
  "fine_tuned_model": null,
  "organization_id": "org-BQxIxn43nwRPlRTFqrCAHzwL",
  "result_files": [],
  "status": "running",
  "validation_file": "file-BocazJt8vBa4rtHRGWroIuvW",
  "training_file": "file-eHq7uKNF4cihXKmj5IIbGHgl",
  "hyperparameters": {
    "n_epochs": 3
  },
  "trained_tokens": null,
  "error": null
}
{
  "object": "list",
  "data": [
    {
      "object": "fine_tuning.job.event",
      "id": "ftevent-6gXYkcjhiv20y55coGqocBJq",
      "created_at": 1699091435,
      "level": "info",
      "message": "Fine-tuning job started",
      "data": null,
      "type": "message"
    },
    {
      "object": "fine_tuning.job.event",
      "id": "ftevent-UZ97zWAZxbtTLO5ThURThx7K",
      "created_at": 1699091434,
      "level": "info",
      "message": "Files validated, moving job to queued state",
      "data": {},
      "type": "message"
    },
    {
      "object": "fine_tuning.job.event",
      "id": "ftevent-6jLEeVT4XaR06U3Q7EWxo6C8",
      "created_at": 1699091401,
      "level": "info",
      "message": "Validating training file: file-eHq7uKNF4cihXKmj5IIbGHgl and validation file: file-BocazJt8vBa4rtHRGWroIuvW",
      "data": {},
      "type": "message"
    },
    {
      "object": "fine_tuning.job.event",
      "id": "ftevent-fzchgBMOiZPFxUCi7JiBQln5",
      "created_at": 1699091401,
      "level": "info",
      "message": "Created fine-tuning job: ftjob-xhaP1dDASdwldTCUoMYllWUi",
      "data": {},
      "type": "message"
    }
  ],
  "has_more": false
"""