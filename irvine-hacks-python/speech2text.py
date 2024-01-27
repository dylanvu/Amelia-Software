import speech_recognition as sr
from dotenv import load_dotenv
import os
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

def listen(recognizer, microphone, OPENAI_API_KEY):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")
    with microphone as source:
        print("Say something!")
        audio = recognizer.listen(source)
        print("done listening!")
    # recognize speech using Whisper API
    try:
        transcription = recognizer.recognize_whisper_api(audio, api_key=OPENAI_API_KEY)
        print(f"Whisper API thinks you said: {transcription}")
    except sr.RequestError as e:
        print("Could not request results from Whisper API")
    return transcription


def listen_until_keyword(api_key, keywords, recognizer, microphone):
    while True:
        transcription = listen(recognizer, microphone, api_key)
        # check if the transcription contains the keyword
        print("wake-word-listen:",transcription)
        if any(keyword.lower() in transcription.lower() for keyword in keywords):
            print("Keyword detected...")
            break
    
    # Start recording longer segments until a pause is detected
    transcription = listen(recognizer, microphone, api_key)
    print("speech-to-text:",transcription)
    # check if the user is done talking?

    # common_hallucination = 'thank you for watching'
    # if not transcription.text.strip() or transcription.text.lower() == '.' or common_hallucination.lower() in transcription.text.lower():
    #     print("Pause detected, stopping recording.")
    #     break
    # print("Transcription:", transcription.text)

    return transcription

def main():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    simliar_wakeup_words = [
        "Hey, Emilia",
        "A, Amelia",
        "Say, Amelia",
        "Hey, Familia",  
        "Hey, Ophelia",
        "Hey, Camellia",
        "They, Amelia",
        "Hey, Amelia",
        "Hey, Cecilia",
        "Play, Amelia",
        "Stay, Amelia",
        "May, Amelia",
        "Lay, Amelia",
        "Hey, Media",
        "Hey, Amalia",
        "Hey, Emilio"
    ]
    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    adjust_ambient_noise(recognizer, microphone)
    listen_until_keyword(OPENAI_API_KEY, simliar_wakeup_words, recognizer, microphone)
    # listen(recognizer, microphone, OPENAI_API_KEY)

if __name__ == '__main__':
    main()