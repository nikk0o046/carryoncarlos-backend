from langchain import PromptTemplate

from time_template import time_template

def create_time_params(user_request):
    template = time_template

    prompt = PromptTemplate.from_template(template)
    
    return prompt.format(user_request=user_request)

print(create_time_params("I want to go home"))
