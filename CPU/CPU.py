import psutil
import pyttsx3
engine = pyttsx3.init()
def speak(audio):
  engine.say(audio)
  engine.runAndWait()

def cpu():
    usage = str(psutil.cpu_percent())
    print("CPU is at "+usage)
    speak("CPU is at "+usage)
    battery_left = str(psutil.sensors_battery()) 
    speak("The battery percent is ")
    speak(battery_left)
    print(battery_left)
