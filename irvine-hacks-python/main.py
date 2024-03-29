from dotenv import load_dotenv
import os
import requests
import json
from camera import sendImage
from text2speech import textToSpeech
from rpiSerial import sendCommand
import speech2text
import speech_recognition as sr
import time
import serial

load_dotenv()  # take environment variables from .env.

textToSpeech("Give me a moment to figure out what's going on.")


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

port = "/dev/ttyUSB0" # rpi
# port = "COM8" # windows
ser = serial.Serial(port=port, baudrate=115200, timeout=0.1)
time.sleep(2)

commandDictionary = {
    "FORWARD": "0",
    "BACKWARD": "1",
    "TURNLEFT": "2",
    "TURNRIGHT": "3",
    "WAIT": "4"
}

### start 
# question = "What do you know about Mount Everest?"
active = True


# mode == 1: lovermode
# mode == 2: travelmode
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# create recognizer and mic instances
recognizer = sr.Recognizer()
microphone = sr.Microphone()
question, mode = speech2text.init(OPENAI_API_KEY, recognizer, microphone)
print("past init")
# mode = 1 --> travel
# mode = 2 --> lovers
prompt_file = 'travel_prompt.txt' if mode == 0 else 'partner_prompt.txt'
print("Mode:", mode)

too_many_repeat_movements = 0
current_movement = ''

# question = transcription

while active:
    if mode is None:
        textToSpeech("What should I do now?")
        print("What should I do now?") # debug
        # question = input()
        # question = speech2text.await_listen(OPENAI_API_KEY, recognizer, microphone)
        question = speech2text.listen_until_wake(OPENAI_API_KEY, recognizer, microphone)
        
    mode = None

    # the meat of the loop
    isContinue = True
    continuing = False

    while isContinue:
        
        prompt = [
            {
                "text": "Who are you?"
            },
            {
                "text": open(prompt_file, 'r').read()
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

        # special text if Amelia is acting autonomously
        if continuing:
            textToSpeech("I need to figure out what to do next.")
        else:
            textToSpeech("Let me think...")

        res = requests.post(GEMINI_ENDPOINT, json = reqObj)

        # using the stop sequence, add a } to after
        # print(res.json(),'\n') # DEBUG
        try:
            actionString = res.json()["candidates"][0]["content"]["parts"][0]["text"] + "}"
        except Exception as e:
            print(res.json())
            print("actionString exception")
            if continuing:
                textToSpeech("I'm confused now. I'll stop what I'm doing.")
            else:
                textToSpeech("I didn't quite catch that, sorry!")
            continue
        
        action = None
        try:
            # turn the json string to an object
            action = json.loads(actionString)
        except Exception as e:
            print(actionString)
            print(action) # DEBUG
            if continuing:
                textToSpeech("I'm confused now. I'll stop what I'm doing.")
            else:
                textToSpeech("I didn't quite catch that, sorry!")
            continue
        # print() # DEBUG

        # process all the actions
        speak = action["SPEAK"]
        move = action["MOVE"]
        see = action["SEE"]

        # implement speaking
        if len(speak) > 0:
            textToSpeech(speak)
            print(speak)

        # if speak contains 'goodbye' end program instantly
        if 'goodbye' in speak.lower():
            active = False
            break

        if move != '4' and current_movement == move:
            too_many_repeat_movements += 1
        else:
            too_many_repeat_movements = 0
        if too_many_repeat_movements >= 2:
            isContinue = 'false' # TESTTTTTTT

        # implement movement
        if len(move.lower()) > 0:
        #     # TODO - send an ascii character 0 to 4 to RX TX
            commandChar = commandDictionary[move]
            sendCommand(commandChar, ser)
            print(move)

        # implement seeing
        picture = ""
        if see.lower() == "true":
            textToSpeech("I'll need to take a look. Please wait!")
            picture = sendImage()
            print("Picture taken")
            textToSpeech("Okay, I finished looking.")

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
            continuing = True
            # the user will prompt it with "CONTINUE"
            question = "CONTINUE"
            if len(picture) > 0:
                # send the photo also
                history.append(
                    {
                        "inlineData": {
                            "mimeType": "image/jpeg",
                            # remove the "data:image/png;base64" part
                            "data": picture
                        }
                    }
                )
        else:
            # no autonomy
            continuing = False

        # print("history:", history) # DEBUG