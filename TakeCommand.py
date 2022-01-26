import speech_recognition as sr 
import pyttsx3
engine = pyttsx3.init()
def speak(audio):
  engine.say(audio)
  engine.runAndWait()
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening..")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing..")
        query = r.recognize_google(audio, language='en-us')
        print(query)

    except Exception as e:
        speak("Unable to Recognize your voice. Make sure that you have a good internet connection.")
        return "None"

    return query
