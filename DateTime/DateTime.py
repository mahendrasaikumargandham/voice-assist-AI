import pyttsx3
import datetime

engine = pyttsx3.init()
def speak(audio):
  engine.say(audio)
  engine.runAndWait()
def time():                                                         
  time = datetime.datetime.now().strftime("%I:%M:%S")
  speak(time)                                                      
  
def date():                                                        
  date = str(datetime.datetime.now().day)
  month = str(datetime.datetime.now().month)
  year = str(datetime.datetime.now().year)
  speak(date)                                                    
  speak(month)                                                      
  speak(year)                                                   
  
  
  
