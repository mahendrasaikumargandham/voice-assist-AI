import pyttsx3
import pyjokes

engine = pyttsx3.init()
def speak(audio):
  engine.say(audio)
  engine.runAndWait()

def jokes():
    speak(pyjokes.get_joke())                       
