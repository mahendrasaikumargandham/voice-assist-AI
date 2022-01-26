import pyttsx3
import smtplib

engine = pyttsx3.init()
def speak(audio):
  engine.say(audio)
  engine.runAndWait()

def sendMail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 'passwd')
    server.ehlo()
    server.starttls()
    server.login('your_mail@gmail.com', 'passwd')
    server.sendmail('your_mail@gmail.com', to, content)
    server.close()
