import speech_recognition as sr
from dotenv import load_dotenv
import os
from text2speech import textToSpeech
load_dotenv()



# def find_microphone_index(device='USBAudio2.0'):
#     mics = sr.Microphone.list_microphone_names()
#     mic_index = None
#     for i, mic_name in enumerate(mics):
#         if 'USBAudio2.0' == mic_name:
#             mic_index = i
#             break
#     if mic_index is None:
#         print("Could not find 'USBAudio2.0' microphone")
#         mic_index = 0
#     return mic_index



def adjust_ambient_noise(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")
    with microphone as source:
        print("Adjusting noise...")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Done adjusting!")

def listen(recognizer, microphone, OPENAI_API_KEY, time_limit=30):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")
    with microphone as source:
        print("Say something!")
        # if time_limit:
        audio = recognizer.listen(source=source, phrase_time_limit=time_limit)
        # else:
        #     audio = recognizer.listen(source,phrase_time_limit=60)
        print("done listening!")
    # recognize speech using Whisper API
    try:
        transcription = recognizer.recognize_whisper_api(audio, api_key=OPENAI_API_KEY)
        print(f"Whisper API thinks you said: {transcription}")
    except sr.RequestError as e:
        print("Could not request results from Whisper API")
    return transcription


# listens until keyword,
# stops looking for keyword after it is found
def listen_until_keyword(api_key, keywords, recognizer, microphone):
    while True:
        transcription = listen(recognizer, microphone, api_key, time_limit=3)
        print("wake-word-listen:",transcription)
        keyword = None
        
        # 2d array
        if isinstance(keywords, list) and any(isinstance(item, list) for item in keywords):
            for greeting in keywords[0]:
                if greeting.lower() in transcription.lower() and \
                any(name.lower() in transcription.lower() for name in keywords[1]):
                    print("Keyword detected...")
                    keyword = greeting.lower()
                    print("keyword")
                    break
            if keyword:
                break
        # 1d array
        else:
            for greeting in keywords:
                if greeting.lower() in transcription.lower():
                    print("Keyword detected...")
                    keyword = greeting.lower()
                    print("keyword")
                    break
            if keyword:
                break
        textToSpeech("Sorry can you say that again?")

    return transcription, keyword

# Starts Up the seech to text, returns the mode Amelia should talk to you in
def startUp(api_key, recognizer, microphone):
    # listensforNameKeyword
    # "what do you want me to do today / what mode"
    # listens for mode
    # sets mode
    
    # initializing words list
    simliar_wakeup_words = [
        [
        "Hey",
        "A",
        "Say",
        "Hey",
        "Hey",
        "Hey",
        "They",
        "Hey",
        "Hey",
        "Play",
        "Stay",
        "May",
        "Lay",
        "Hey",
        "Hey",
        "Hey"
        ],
        [
        "Emilia",
        "Amelia",
        "Amelia",
        "Familia",
        "Ophelia",
        "Camellia",
        "Amelia",
        "Amelia",
        "Cecilia",
        "Amelia",
        "Amelia",
        "Amelia",
        "Amelia",
        "Media",
        "Amalia",
        "Emilio"
    ]]
    
    mode_words = [
        "Girlfriend",
        "Boyfriend",
        "Partner",
        "Lover",
        "Travel Buddy",
        "Travel Mode",
        "Travel Companion",
        "Travel Buddy"
    ]
    
    modes_dictionary = {
        "lovermode_words": ["girlfriend", "boyfriend", "partner", "lover"],
        "travel_words": ["travel", "gravel"]
    }
    
    # inital wake up (call for amelia)
    listen_until_keyword(api_key, simliar_wakeup_words, recognizer, microphone)
    # response (ask for the mode)
    textToSpeech("Hey what do you want me to do today?")
    # wait for user to give the mode
    transcription, keyword = listen_until_keyword(api_key, mode_words, recognizer, microphone)
    
    mode = 0
    # mode 1 = LOVER, mode 2 = TRAVEL
    if keyword in modes_dictionary["lovermode_words"]:
        print("1", keyword)
        mode = 1
    if keyword in modes_dictionary["travel_words"]:
        print("2", keyword)
        mode = 2
    
    return transcription, mode

def mainLoop(api_key, recognizer, microphone):
    # always listens until a pause
    # generate response
    
    # continues until it deactivates somehow
    while True:
        # listens until a pause
        transcription = listen(recognizer, microphone, api_key)
        # get a response from GEMINI
        

# returns transcription, mode
def init(api_key, recognizer, microphone):
    OPENAI_API_KEY = api_key
    adjust_ambient_noise(recognizer, microphone)
    # call start up
    return startUp(OPENAI_API_KEY, recognizer, microphone)


def listen_until_wake(api_key, recognizer, microphone):
    # initializing words list
    simliar_wakeup_words = [
        [
        "Hey",
        "A",
        "Say",
        "Hey",
        "Hey",
        "Hey",
        "They",
        "Hey",
        "Hey",
        "Play",
        "Stay",
        "May",
        "Lay",
        "Hey",
        "Hey",
        "Hey"
        ],
        [
        "Emilia",
        "Amelia",
        "Amelia",
        "Familia",
        "Ophelia",
        "Camellia",
        "Amelia",
        "Amelia",
        "Cecilia",
        "Amelia",
        "Amelia",
        "Amelia",
        "Amelia",
        "Media",
        "Amalia",
        "Emilio"
    ]]
    while True:
        transcription = listen(recognizer, microphone, api_key)
        print("wake-word-listen:",transcription)
        keyword = None
        for greeting in simliar_wakeup_words[0]:
            if greeting.lower() in transcription.lower() and \
            any(name.lower() in transcription.lower() for name in simliar_wakeup_words[1]):
                print("Keyword detected...")
                keyword = greeting.lower()
                print("keyword")
                break
        if keyword:
            index = transcription.lower().find(keyword)
            new_transcription = transcription[index:]
            break
    return new_transcription
        


def await_listen(OPENAI_API_KEY, recognizer, microphone, pauses=3):
    for _ in range(pauses):
        transcription = listen(recognizer, microphone, OPENAI_API_KEY)
        if len(transcription) > 0:
            return transcription
    return "goodbye"


def main():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    adjust_ambient_noise(recognizer, microphone)
    # call start up
    startUp(OPENAI_API_KEY, recognizer, microphone)
    # main loop
    mainLoop(OPENAI_API_KEY, recognizer, microphone)
    

if __name__ == '__main__':
    main()