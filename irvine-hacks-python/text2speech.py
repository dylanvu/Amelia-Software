# TODO:
# def TextToSpeech(text, lang_code, check_translate):
    # inputs: text (str), lang (str), check_translate (bool)
    # if check_translate is true 
        # -> translate the text to the desired language       
    # plays out the text to one's speakers
    
# def TranslateText(text, langFrom, langTo):
    # langFrom, langTo
    # convert text to the language we want to translate to
    # return the converted text
    
# def listVoices(lang_code):
    # lists out google cloud api voices it has

from google.cloud import texttospeech
from google.cloud import translate_v2 as translate
from playsound import playsound
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../google_secret_key.json'

# Function to turn Text into speech
# text: (str) to be played out
# langTo: (str) that has google cloud translate language code, on to which language the text should be translated to
# check_translate: (boolean) check if we need to translate
# filename: (str) that has the filename we want to write the outputted mp3 to
def TextToSpeech(text, langTo, check_translate, filename):
    # initiate text to speech client
    client = texttospeech.TextToSpeechClient()
    translate_client = translate.Client()

    # if we translate translate here
    if check_translate == True:
        # translate the text
        text = translateText(text, langTo)
        
        #get correct voice bank
        voiceArr = findCorrectVoice(langTo)
        print(voiceArr[0], voiceArr[1])
    
    print(text)
    # choose text to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    voice = texttospeech.VoiceSelectionParams(
        
        name=voiceArr[0],  # Replace with the actual name of the female voice
        language_code=voiceArr[1] # for translation change code
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file filename')
        out.close()
    
    # play sound to speakers
    playsound(filename)

# translateText -> takes in str and translate it to desired language, returns string of translated text
# text: (str) text to be translated
# langTo: (str) language code to be translated to
def translateText(text, langTo):
    translate_client = translate.Client()
    
    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=langTo)["translatedText"]

    return result

# function to grab voice selection and language code
# lang_code: (str) string that says what language it should be translated to
# returns an array where item 1 is the voice name and item2 is the language code
def findCorrectVoice(lang_code):
    client = texttospeech.TextToSpeechClient()

    # perform the list voices request
    response = client.list_voices(language_code=lang_code)

    # display the voices
    for voice in response.voices:
        if texttospeech.SsmlVoiceGender(voice.ssml_gender).name == "FEMALE":
            return [voice.name, voice.language_codes[0]]


# TextToSpeech("I am a woman", "en-US", False, "output.mp3")
# TextToSpeech("I am a woman", "es", True, "output.mp3")

# print(translateText("I am a woman", "vi"))

# listVoices("vi")

# print(findCorrectVoice("vi"))



