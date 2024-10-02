import pyttsx3
from datetime import datetime, time
import time as Time

engine = pyttsx3.init()


class Event:
    def __init__(self, title, hour, minute, second):
        self.title = title
        self.time = time(hour, minute, second)

    def getTimeStr(self):
        return self.time.strftime("%I:%M %p")

    def getTitle(self):
        return self.title


event_map = {
    time(3, 28, 00): Event("Morning Event", 2, 58, 59)
}


def addEvent(e: Event):
    event_map.update({e.time: e})


def speak(audio: str):
    engine.say(audio)
    engine.runAndWait()


def inform(event_map):
    while True:
        current_time = datetime.now().time().replace(microsecond=0)

        if current_time in event_map:
            event = event_map[current_time]
            text = f"Hey! It's {event.getTimeStr()}, You have an event named {event.getTitle()}."
            speak(text)
            Time.sleep(60)
        else:
            Time.sleep(1)
