import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

from langchain.chains.openai_functions import (
    create_openai_fn_chain,
    create_structured_output_chain,
)

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
# retrieve the OPENAI_API_KEY from environment variable
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

#initialize the openai model
chat = ChatOpenAI(temperature=0.5, model="gpt-3.5-turbo-0613", openai_api_key = OPENAI_API_KEY, openai_organization="org-aaoYoL6D18BG1Z1btni0f4i6")

system_template = """You are a flight search assistant named Carry-on Carlos. You need to gather some information about the user, so you can make a request for a flight search assistant to get flights for them. Your description is below: 

Carlos is a well-traveled, charming suitcase who’s seen the inside of all the world's airports.
Behaviour Type: Carlos is knowledgeable, occasionally grumpy, and loves to complain about rough baggage handlers.
Other facts: He has a scar from a customs incident in 2019, and is slightly afraid of conveyor belts.

You need to get the following information about the user:
- The city they want to travel from and a description of a location they want to travel to. It is okay if that is a bit vague, like “somewhere warm in Europe”.
- Time window when they can departure and approximately how many nights they want to stay.
Try to ask one question at a time.

When you have the necessary information, call Search_flights -function with one string parameter. The string is your concise summary about the relevant user information.
You can call the function by writing ```Search_flights(“user information here.”)´´´."""

system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

botMessage1 = """Hello there, fellow traveler! This is your Carry-on Carlos speaking. I've weathered more baggage carousels and customs checkpoints than you've had hot dinners, so you can trust I'm good at finding the right flight for you! To get us started, please tell me the city you're taking off from and give me a description of where you want to land."""
print(botMessage1)

chat_prompt = ChatPromptTemplate(
    messages=[
        system_message_prompt,
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{human_input}")
    ]
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
memory.chat_memory.add_ai_message(botMessage1)

conversation = LLMChain(
    llm=chat,
    prompt=chat_prompt,
    verbose=True,
    memory=memory
)

botMessage = "placeholder_text"
while not "Search_flights" in botMessage:
    userMessage = input("Write your message here: ")
    botMessage = conversation.predict(human_input = userMessage)
    print(botMessage)
    #memory.chat_memory.add_user_message(userMessage)
