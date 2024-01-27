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
                "text": open("prompt.txt", 'r').read()
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