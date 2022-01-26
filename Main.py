import CPU.CPU                                                                           # importing cpu() function from CPU.py
import DateTime.DateTime                                                                  
import Jokes.Jokes                                                                         # importing jokes() from Jokes.py
import ScreenShots.ScreenShot                                                                      # importing screenshot() from Screenshot.py
import MailSender.SendMail                                                                       # importing sendMail() from SendMail.py
from TakeCommand import *                                                                     # importing takeCommand() from TakeCommand.py
import pyttsx3
import webbrowser as wb
import wikipedia
import os

engine = pyttsx3.init()
def speak(audio):
  engine.say(audio)
  engine.runAndWait()
  

if __name__ == "__main__":                                                                    # main function of the project.                                               
    while True:
        query = takeCommand().lower()

        if 'time' in query:                                                                   # if there is a word 'time' in the query, then it will call the time().
            DateTime.DateTime.time()

        elif 'date' in query:                                                                 # It will call date() when there is a word 'date' in your query.
            DateTime.DateTime.date()

        elif 'wikipedia' in query:                                                            # it will search on wikipedia without any opening of browser.
            speak("Searching..")
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences=2)
            print(result)
            query(result)

        elif 'send mail' in query:                                                            # sendMail() excutes from the SendMail.py file
            try:
                speak("What should I send? ")
                content = takeCommand()
                to = 'Client_mail_address@domain.com'
                MailSender.SendMail.sendMail(to, content)
                speak(content)
                speak("E mail has been sent!")
            except Exception as e:
                print(e)
                speak("Unable to send Email, Please Check your internet connection")

        elif 'search in chrome' in query:                                                      # It will opens the chrome and search for the results.
            speak("What should I search?")
            chromepath = 'your chrome application path' 
            search = takeCommand().lower()
            wb.get(chromepath).open_new_tab(search)

        elif 'logout' in query:                                                                # It will logout if you give logout as a word input
            os.system("Shutdown -l")

        elif 'shutdown' in query:                                                              # It will shutdown the system. Make sure that all the data is saved in your computer if you want to shutdown the computer.
            os.system("Shutdown /s /t 1")                                                      # try at your own risk, because some data may not come back after the shutdown process.

        elif 'restart' in query:                                                           # It will restart the computer if you give restart as the command.
            os.system("Shutdown /r /t 1")

        elif 'play songs' in query:
            songs_dir = 'D:\\Music'                                                            # in songs_dir variable you can add your own path of music.
            songs = os.listdir(songs_dir)
            os.startfile(os.path.join(songs_dir, songs[0]))
            
        elif 'remember' in query:
            speak("What should I remember? ")
            data = takeCommand()
            speak("you said me to remember "+data)
            remember = open('Data/data.txt', 'w')
            remember.write(data)
            remember.close()                                                                    

        elif 'do you know' in query:                                                           # If there is a command 'do you know', then it will check if there is anything saved in the data.txt file
            remember = open('Data/data.txt', 'r')                                                   # If there is anything in the file, then it will speak out the saved ones.
            speak("You said me to remember that"+remember.read())                                   

        elif 'screenshot' in query:                                                             # It will take the screenshot and saves the screenshot in the same directory.
            ScreenShots.ScreenShot.screenshot()
            speak("Screenhot taken")

        elif 'cpu' in query:                                                                    # speaks the state of CPU in your computer.
            CPU.CPU.cpu()

        elif 'joke' in query:                                                                   # speaks a random joke from pyjokes package in Package.py file
            Jokes.Jokes.jokes()

        elif 'offline' in query:                                                                # quits the program when there is a word 'offline' in your query.
            quit()
