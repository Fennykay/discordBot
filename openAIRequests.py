from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('OPENAI_API')  # Correct variable name
openai = OpenAI(api_key=api_key)  # Pass the API key to the client constructor
model = "gpt-4o"


def get_response_trump(message, user="nobody"):
    file = open("./resources/prompts/donaldTrump", "r")
    initial_prompt = file.read()  # Read the initial prompt

    if user == "nobody":
        messages = [{"role": "system", "content": initial_prompt},
                    {"role": "user",
                     "content": f"{message}"}]
    else:
        # Define the initial messages list with the initial prompt
        messages = [{"role": "system", "content": initial_prompt},
                    {"role": "user",
                     "content": f"{message} The user's name, that you are currently talking to is {user}"}]
        # Append the user message to the existing messages list

    completion = openai.chat.completions.create(
        model=model,
        messages=messages
    )
    response = completion.choices[0].message.content
    return response


def get_response_tutor(message, user):
    file = open("./resources/prompts/Tutor.txt", "r")
    initial_prompt = file.read()  # Read the initial prompt

    # Define the initial messages list with the initial prompt
    messages = [{"role": "system", "content": initial_prompt},
                {"role": "user", "content": f"{message} The user's name, that you are currently talking to is {user}"}]
    # Append the user message to the existing messages list

    completion = openai.chat.completions.create(
        model=model,
        messages=messages
    )
    response = completion.choices[0].message.content
    return response


def get_god_response(message, user):
    file = open("./resources/prompts/God", "r")
    initial_prompt = file.read()  # Read the initial prompt

    # Define the initial messages list with the initial prompt
    messages = [{"role": "system", "content": initial_prompt},
                {"role": "user", "content": f"{message} The user's name, that you are currently talking to is {user}"}]

    completion = openai.chat.completions.create(
        model=model,
        messages=messages
    )
    response = completion.choices[0].message.content
    return response


def summarize_cookiing_recipe(message):
    file = open("./resources/prompts/donaldTrump", "r")
    initial_prompt = file.read()  # Read the initial prompt

    messages = [
        {"role": "system", "content": initial_prompt + ". You primary goal is to read the current recipe provided"
                                                       "and to summarize it in a way that is easy to understand"
                                                       ". Be sure to included the ingredients and the instructions."
         },
        {"role": "user", "content": f"{message}"}]

    completion = openai.chat.completions.create(
        model=model,
        messages=messages
    )
    response = completion.choices[0].message.content
    return response


def describe_image(image_url):
    file = open("./resources/prompts/donaldTrump", "r")
    initial_prompt = file.read()  # Read the initial prompt

    messages = [
        {"role": "system", "content": initial_prompt + ". You primary goal is to describe the image provided. Be sure to"
                                                       "be very judgemental and opinionated."},
        {"role": "user", "content": [
            {"type": "image_url",
             "image_url": {
                 "url": image_url,
             }},
        ]}
        ]

    completion = openai.chat.completions.create(
        model=model,
        messages=messages
    )
    response = completion.choices[0].message.content
    return response
