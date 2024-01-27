from dotenv import load_dotenv
import os
import requests
import json
from camera import takePic
from text2speech import textToSpeech

load_dotenv()  # take environment variables from .env.

KEY = os.getenv("GEMINI_API_KEY")
# GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={KEY}"
GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key={KEY}"


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

question = "What landmark is this?"

# the meat of the loop
isContinue = True

while isContinue:

    prompt = [
        {
            "text": "Who are you?"
        },
        {
            "text": open("prompt.txt", 'r').read()
        },
        {
            "text": "Ignore this photo."
        },
        {
            "inlineData": {
                "mimeType": "image/png",
                # remove the "data:image/png;base64" part
                "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAACAQMAAACjTyRkAAAAIGNIUk0AAHomAACAhAAA+gAAAIDoAAB1MAAA6mAAADqYAAAXcJy6UTwAAAAGUExURQUDAf///woIE9sAAAABYktHRAH/Ai3eAAAACXBIWXMAABJ0AAASdAHeZh94AAAAB3RJTUUH6AEbCgoBDMSXqwAAAAFvck5UAc+id5oAAAAMSURBVAjXY2BgYAAAAAQAASc0JwoAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjQtMDEtMjdUMTA6MDk6NDYrMDA6MDAomuxkAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDI0LTAxLTI3VDEwOjA5OjQ2KzAwOjAwWcdU2AAAACh0RVh0ZGF0ZTp0aW1lc3RhbXAAMjAyNC0wMS0yN1QxMDoxMDowMSswMDowMHKksXkAAAAASUVORK5CYII="
            }
        },
        {
            # "role": "model",
            "text": "Ok."
        },
        {
            "text": "From this moment on, you can only speak in the JSON format specified."
        },
        {
            "text": """"
{
    "SPEAK": "I understand.",
    "MOVE" : "WAIT",
    "SEE": "false",
    "continue": "false"
}
            """
        }
    ] + history + [
        # store and repeat the history
        {
            "text": "" + question
        }
    ]

    reqObj = {
        "contents": {"parts": prompt},
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
    # print(res.json())
    actionString = res.json()["candidates"][0]["content"]["parts"][0]["text"] + "}"
    # turn the json string to an object
    action = json.loads(actionString)
    print(action)

    # process all the actions
    speak = action["SPEAK"]
    move = action["MOVE"]
    see = action["SEE"]

    # implement speaking
    if len(speak) > 0:
        textToSpeech(speak)
        print(speak)

    # implement movement
    if move.lower() != "wait":
        # TODO - send an ascii character 0 to 4 to RX TX
        print(move)

    # implement seeing
    picture = ""
    if see.lower() == "true":
        picture = takePic()
        print("Picture taken")

    isContinue = action["continue"].lower() == "true"

    # build the latest memory
    latestUserAction = {
        # "role": "user",
        # "parts": {
        "text": question
        # }
    }


    latestModelAction = {
        # "role": "model",
        # "parts": {
        "text": actionString
        # }
    }

    # TODO: trim memory to not overwhelm the API

    # push to memory for persistence
    history.append(latestUserAction)
    history.append(latestModelAction)

    # if we are continuing
    if isContinue:
        # basically at this point, the API will continue requesting itself
        # the user will prompt it with "CONTINUE"
        question = "CONTINUE"
        if len(picture) > 0:
            # send the photo also
            history.append(
                {
                    "inlineData": {
                        "mimeType": "image/jpg",
                        # remove the "data:image/png;base64" part
                        "data": picture
                    }
                }
            )

    # print(history)