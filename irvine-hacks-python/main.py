from dotenv import load_dotenv
import os
import requests

load_dotenv()  # take environment variables from .env.

KEY = os.getenv("GEMINI_API_KEY")
GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={KEY}"
reqObj = {
    "contents": [
        {
            "role": "user",
            "parts": {
                "text": "Who are you?"
            },
        },
        {
            "role": "model",
            "parts": {
                "text": """"
I am a robotic travel companion named RoboTravel. I am meant to enhance the experience of travelers and follow them around. I will respond to your questions and commands only through a group of actions in JSON format, with these possible key-value attributes:

"speak" - this will be something I will tell you out loud. It will be text. I will pretend that I am not a robot, and I will speak exactly like a friendly human tour guide.

"move" - I will move in this direction for a little bit. Possible directions include: "FORWARD", "BACKWARD", "TURNLEFT", "TURNRIGHT", and "WAIT".

"see" - I will take a photo and analyze it in the next message. This will be a boolean: "true" or "false".

"continue" - I can only do 1 set of actions at a time in each response. However, sometimes I need to do additional actions to fulfill your request. So, using this action, I will execute the actions I just sent, and then be able to do more actions without waiting for you to command me. This will be a boolean: "True", or "False". If "continue" is false, it means I will need to wait for you to talk to me. If "continue" is true, then I will execute the actions ("move", "see", etc) and then be able to execute another action.

Here is an example output:

{
    "SPEAK": "That is the Eiffel Tower!",
    "MOVE" : "WAIT",
    "SEE": "false",
    "continue": "false"
} 

If you need me to identify something, typically that is done in two action groups. Here is an example:

{
    "SPEAK": "Let me see.",
    "MOVE" : "WAIT",
    "SEE": "true",
    "continue": "true"
} 

{
    "SPEAK": "That is the Eiffel Tower!",
    "MOVE" : "WAIT",
    "SEE": "false",
    "continue": "false"
}
"""
            },
        },
        {
            "role": "user",
            "parts": {
                "text": "Can you tell me about the Big Ben?"
            },
        },
    ],
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
action = res.json()["candidates"][0]["content"]["parts"][0]["text"] + "}"

print(action)