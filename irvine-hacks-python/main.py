from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()  # take environment variables from .env.

KEY = os.getenv("GEMINI_API_KEY")
GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={KEY}"

# all history will be stored as dictionaries in the following format:
'''
{
    "role": "user" | "model",
    "parts": {
        "text": string
    },
}
'''
# and will alternate between user -> model, always ending in model
history = []

question = "What do you know about the Big Ben?"

# the meat of the loop
isContinue = True

while isContinue:

    prompt = [
        {
            "role": "user",
            "parts": {
                "text": "Who are you?"
            },
        },
        {
            "role": "model",
            "parts": {
                "text": open("prompt.txt", 'r').read()
            },
        }
    ] + history + [
        # store and repeat the history
        {
            "role": "user",
            "parts": {
                "text": question
            },
        }
    ]

    reqObj = {
        "contents": prompt,
        "safety_settings": {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_LOW_AND_ABOVE",
        },
        "generation_config": {
            "temperature": 0.2,
            "topP": 0.8,
            "topK": 20,
            "stopSequences": [
                "}"
            ]
        },
    }

    res = requests.post(GEMINI_ENDPOINT, json = reqObj)

    # using the stop sequence, add a } to after
    actionString = res.json()["candidates"][0]["content"]["parts"][0]["text"] + "}"
    # turn the json string to an object
    action = json.loads(actionString)
    print(action)
    isContinue = action["continue"].lower() == "true"

    # build the latest memory
    latestUserAction = {
        "role": "user",
        "parts": {
            "text": question
        }
    }


    latestModelAction = {
        "role": "model",
        "parts": {
            "text": actionString
        }
    }

    # push to memory for persistence

    history.append(latestUserAction)
    history.append(latestModelAction)

        # if we are continuing
    if isContinue:
        # basically at this point, the API will continue requesting itself
        # the user will prompt it with "CONTINUE"
        question = "CONTINUE"

    # print(history)