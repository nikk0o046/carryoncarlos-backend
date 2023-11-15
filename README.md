# Carry-on Carlos (Backend)

## Overview

This repository contains the backend for a flight search application that enables users to find cheap flights using natural language queries. The frontend is managed in a separate repository, which you can find [here](https://github.com/nikk0o046/carryoncarlos-frontend/).

The backend uses Large Language Models (LLMs), including OpenAI's GPT-3.5 and GPT-4, to interpret and transform user queries into structured JSON objects. These objects are used to fetch flight data from the kiwi.com API, presenting the cheapest available flights to the user in the frontend.

Check live demo here: [carryoncarlos.com](https://carryoncarlos.com)

## Project Structure

- **app/**: Core application code including the entry point and input parsing logic.
- **api/**: API interaction logic for making requests and handling responses.
- **params/**: Modules for constructing API query parameters from user input.
- **tests/**: Tests to ensure application logic reliability and stability.
- **models/**: Scripts and pretrained models for the LLMs.
- **data/**: Data used for model training and validation.
- Additional files for Docker, environment variables, and dependency documentation and virtual environment.

![ProcessFlowChart](https://github.com/nikk0o046/carryoncarlos-backend/blob/master/ProcessFlowChart.png)

## Technologies Used

- Python, with libraries like json and datetime.
- Flask
- OpenAI
- Docker for containerization.
- Google Cloud (Artifact Registry, Cloud Run, Log Explorer)

## Challenges and Solutions

- **NLP Query Parsing**: Developed a mechanism to accurately convert natural language into structured data.
- **API Interaction**: Created a system for reliable external API interaction.
- **Data Management**: Maintained data integrity for model training.

## Roadmap

- [ ] Call parameter functions asyncronously instead of one after another. Could require moving away from Flask to for example FastAPI. Should improve speed significantly.
- [ ] My backend server goes to sleep due to inactivity and it takes a few seconds for it to wake up after receiving a call. This could be improved by pinging it immediately when someone starts using the site (e.g. selects origin city) so that it would be up and running when the actual query arrives.
- [ ] Move to a testing framework to automate testing as a part of a CI-CD pipeline.
- [ ] Create a CI-CD pipeline
- [ ] Create fine-tuned models for time and duration parameter functions. Input_parser could be fine-tuned later as well.
- [ ] Limit the amount of requests a single user can send for security reasons.
- [ ] Improve error handling throughout the app. Especially important when no flights are found. Another LLM could be used to analyse why flights were not found even if the query is technically ok.
- [ ] Make another API call if first call did not find flights to all specified airports. Happens if first 1000 cheapest flights are dominated by certain destinations.
- [ ] Edit kiwi_output_parser so that it includes a couple of flights per destination instead one just one. For example, the fastest and "the best" besides just cheapest.

## Contact

Niko Virtanen  
niko.virtanen@alumni.aalto.fi
