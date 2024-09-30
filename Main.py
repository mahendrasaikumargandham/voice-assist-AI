import CPU.CPU
import DateTime.DateTime
import Jokes.Jokes
import ScreenShots.ScreenShot
import MailSender.SendMail
from TakeCommand import takeCommand
import pyttsx3
import webbrowser as wb
import wikipedia
import os
import requests
import json
import wolframalpha
import speech_recognition as sr
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import logging
import asyncio
import aiohttp
from dotenv import load_dotenv
import random
import calendar
import pytz
from datetime import datetime
import geocoder

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(filename='assistant.log', level=logging.INFO, format='%(asctime)s - %(message)s')

engine = pyttsx3.init()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Initialize TF-IDF vectorizer
vectorizer = TfidfVectorizer()
stop_words = set(stopwords.words('english'))

# Load intent data
with open('intents.json', 'r') as f:
    intents = json.load(f)

# Prepare intent data for TF-IDF
intent_texts = [' '.join(intent['patterns']) for intent in intents['intents']]
tfidf_matrix = vectorizer.fit_transform(intent_texts)

def get_intent(query):
    query_vector = vectorizer.transform([query])
    similarities = cosine_similarity(query_vector, tfidf_matrix)
    intent_index = np.argmax(similarities)
    return intents['intents'][intent_index]

async def fetch_weather(city):
    api_key = os.getenv('WEATHER_API_KEY')
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            if data["cod"] != "404":
                main = data["main"]
                temperature = main["temp"]
                humidity = main["humidity"]
                description = data["weather"][0]["description"]
                return f"The temperature in {city} is {temperature}°C with {humidity}% humidity. The weather is {description}."
            else:
                return "City not found."

async def get_news():
    api_key = os.getenv('NEWS_API_KEY')
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            articles = data['articles'][:5]
            news_headlines = [article['title'] for article in articles]
            return "Here are the top 5 news headlines:\n" + "\n".join(news_headlines)

def wolframalpha_query(query):
    app_id = os.getenv('WOLFRAMALPHA_APP_ID')
    client = wolframalpha.Client(app_id)
    try:
        res = client.query(query)
        answer = next(res.results).text
        return answer
    except:
        return "I couldn't find an answer to that question."

# New function to get a random quote
def get_random_quote():
    quotes = [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Innovation distinguishes between a leader and a follower. - Steve Jobs",
        "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
        "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
        "The only limit to our realization of tomorrow will be our doubts of today. - Franklin D. Roosevelt"
    ]
    return random.choice(quotes)

# New function to get current location
def get_current_location():
    g = geocoder.ip('me')
    return g.city

# New function to get time in different time zones
def get_time_in_timezone(timezone):
    tz = pytz.timezone(timezone)
    current_time = datetime.now(tz)
    return current_time.strftime("%I:%M %p")

# New function to get calendar for a specific month and year
def get_calendar(year, month):
    cal = calendar.month(year, month)
    return cal

async def main():
    speak("Hello! I'm your advanced virtual assistant. How can I help you today?")
    
    while True:
        query = takeCommand().lower()
        logging.info(f"User query: {query}")

        intent = get_intent(query)
        response = np.random.choice(intent['responses'])
        speak(response)

        if 'time' in query:
            DateTime.DateTime.time()
        
        elif 'date' in query:
            DateTime.DateTime.date()
        
        elif 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            try:
                result = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(result)
                speak(result)
            except wikipedia.exceptions.DisambiguationError as e:
                speak("There are multiple results. Can you be more specific?")
            except wikipedia.exceptions.PageError:
                speak("Sorry, I couldn't find any information on that topic.")
        
        elif 'send mail' in query:
            try:
                speak("What should I send?")
                content = takeCommand()
                to = 'Client_mail_address@domain.com'
                MailSender.SendMail.sendMail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                logging.error(f"Error sending email: {str(e)}")
                speak("Unable to send Email. Please check your internet connection.")
        
        elif 'search in chrome' in query:
            speak("What should I search?")
            chromepath = 'your chrome application path'
            search = takeCommand().lower()
            wb.get(chromepath).open_new_tab(search + '.com')
        
        elif 'logout' in query:
            os.system("shutdown -l")
        
        elif 'shutdown' in query:
            os.system("shutdown /s /t 1")
        
        elif 'restart' in query:
            os.system("shutdown /r /t 1")
        
        elif 'play songs' in query:
            songs_dir = 'D:\\Music'
            songs = os.listdir(songs_dir)
            os.startfile(os.path.join(songs_dir, songs[0]))
        
        elif 'remember' in query:
            speak("What should I remember?")
            data = takeCommand()
            speak("You said me to remember " + data)
            remember = open('Data/data.txt', 'a')
            remember.write(data + '\n')
            remember.close()
        
        elif 'do you know anything' in query:
            remember = open('Data/data.txt', 'r')
            speak("You said me to remember that " + remember.read())
        
        elif 'screenshot' in query:
            ScreenShots.ScreenShot.screenshot()
            speak("Screenshot taken")
        
        elif 'cpu' in query:
            CPU.CPU.cpu()
        
        elif 'joke' in query:
            Jokes.Jokes.jokes()
        
        elif 'weather' in query:
            speak("Which city's weather would you like to know?")
            city = takeCommand()
            weather_info = await fetch_weather(city)
            speak(weather_info)
        
        elif 'news' in query:
            news = await get_news()
            speak(news)
        
        elif 'calculate' in query:
            question = query.replace('calculate', '')
            answer = wolframalpha_query(question)
            speak(answer)
        
        # New feature: Get a random quote
        elif 'quote' in query:
            quote = get_random_quote()
            speak(quote)
        
        # New feature: Get current location
        elif 'where am i' in query:
            location = get_current_location()
            speak(f"Based on your IP address, you are currently in {location}")
        
        # New feature: Get time in different time zones
        elif 'time in' in query:
            city = query.split('time in', 1)[1].strip()
            try:
                time = get_time_in_timezone(city)
                speak(f"The current time in {city} is {time}")
            except:
                speak(f"Sorry, I couldn't find the time zone for {city}")
        
        # New feature: Get calendar
        elif 'calendar' in query:
            speak("For which year and month do you want the calendar?")
            year_month = takeCommand()
            try:
                year, month = map(int, year_month.split())
                cal = get_calendar(year, month)
                print(cal)
                speak(f"I've displayed the calendar for {calendar.month_name[month]} {year}")
            except:
                speak("Sorry, I couldn't understand the year and month. Please try again.")
        
        elif 'offline' in query:
            speak("Goodbye! Have a great day!")
            break

if __name__ == "__main__":
    asyncio.run(main())
