import pyttsx3
import pyautogui

engine = pyttsx3.init()
def speak(audio):
  engine.say(audio)
  engine.runAndWait()

def screenshot():
    img = pyautogui.screenshot()
    img.save(r'VoiceAssist\ScreenShots\Snaps\ScreenShot.png')
