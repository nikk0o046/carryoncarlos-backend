# Carry-on Carlos (Backend)

## Overview

This repository contains the backend for a flight search application that enables users to find cheap flights using natural language queries. The frontend is managed in a separate repository, which you can find [here](https://github.com/nikk0o046/carryoncarlos-frontend/).

The backend uses Large Language Models (LLMs), including OpenAI's GPT-3.5 and GPT-4, to interpret and transform user queries into structured JSON objects. These objects are used to fetch flight data from the kiwi.com API, presenting the cheapest available flights to the user in the frontend.

Check live demo here: [carryoncarlos.com](https://carryoncarlos.com)

## How to use it

- Click "From:" and start typing the name of the city you're departing from. Click a suggestion that appears.
- Select the amount of travelers
- Write in the text box where you want to go an when. This can include multiple destinations and a longer time frame. You can also add stuff like, "direct flights."
- Click "Search" from the bottom of the page. Searching can take about 30 seconds.
- You get the cheapest flight per city with a booking link. Links lead to kiwi.com where you can proceed with booking.

## Project Structure

### flights_function/:

- **main.py**: Core application code including the entry point and input parsing logic.
- **input_parser.py**: Modifies the input so that rest of the functions work better.
- **api/**: API interaction logic for making requests and handling responses.
- **params/**: Modules for constructing API query parameters from user inputs.
- **tests/**: Tests for individual functions as well as the whole app.
- **fine-tuning/**: Scripts to create and validate data and fine-tune OpenAI models.
- **data/**: Data used for prompting and model training and validation.
- Additional files for Docker, .gitignore and dependency documentation. Also files that are not included in the public repo for environment variables and virtual environment.

## How it works

Frontend sends your query to the backend with departure city and the amount of travelers. Your query is first modified to make it concise and adhere to a standardized structure. The formatted query is then used to call multiple params functions, that call OpenAI's API to get a response back. A valid json object is extracted from each response. There object are combined to create a final search query for Kiwi.com's search API. The response is also handled so only the most relevant flights and fields (of the object) are sent back to the frontend.

### Function to create destination parameters

This is a quick overview on how this function works. Duration and time parameters are created similarly. The main difference is that destination function uses a fine-tuned model, while duration and time functions use a few-shot prompting technique.

- User query (modified by input_parser) is sent to the fine-tuned GPT-3.5 turbo model with system instruction.
- The instructions use ReAct (Reason + Act) framework. This means that the model is instructed to first outline its thought process and only then the answer. The "answer" is a list of IATA airport codes, such as "HEL" for Helsinki. GPT-3.5 and GPT-4 models know these codes pretty well by heart without fine-tuning or RAG (Retrieval Augmented Generation).
- The list of airport codes is extracted from the response using regex and turned to json format, which is then sent forward in the process.

![ProcessFlowChart](https://github.com/nikk0o046/carryoncarlos-backend/blob/master/ProcessFlowChart.png)

## Technologies Used

- Python (3.11.4), with libraries such as json and datetime.
- Flask, Flask-Cors
- OpenAI
- Docker
- Google Cloud (Artifact Registry, Cloud Run, Logging)

## Roadmap

- [ ] Call parameter functions asynchronously instead of one after another. Could require moving away from Flask to for example FastAPI. Should improve speed significantly.
- [ ] My backend server goes to sleep due to inactivity and it takes a few seconds for it to wake up after receiving a call. This could be improved by pinging it immediately when someone starts using the site (e.g. selects origin city) so that it would be up and running when the actual query arrives.
- [ ] Move to a testing framework to automate testing as a part of a CI-CD pipeline.
- [ ] Create a CI-CD pipeline
- [ ] Create fine-tuned models for time and duration parameter functions. Input_parser could be fine-tuned later as well.
- [ ] Limit the amount of requests a single user can send for security reasons.
- [ ] Improve error handling throughout the app. Especially important when no flights are found. An another LLM could be used to analyse why flights were not found even if the query is technically ok.
- [ ] Make another API call if first call did not find flights to all specified airports. Happens if first 1000 cheapest flights are dominated by certain destinations.
- [ ] Edit kiwi_output_parser so that it includes a couple of flights per destination instead of just one. For example, the fastest and "the best" besides just cheapest.

## Contact

Niko Virtanen  
niko.virtanen@alumni.aalto.fi
