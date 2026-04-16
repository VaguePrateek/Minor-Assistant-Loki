import speech_recognition as sr
import pyttsx3 as sx
import webbrowser
import music_lib
import requests
import datetime
import wikipedia
import os
from dotenv import load_dotenv

load_dotenv()

recognizer = sr.Recognizer()

def speak(text):
    engine = sx.init()
    engine.say(text)
    engine.runAndWait()



def command_execution(command):
    command = command.lower()
    
    if "open youtube" in command:
        webbrowser.open("https://www.youtube.com")

    elif "open google" in command:
        webbrowser.open("https://www.google.com")

    elif "open instagram" in command:
        webbrowser.open("https://instagram.com")

    elif "open facebook" in command:
        webbrowser.open("https://www.facebook.com")

    elif "open linkedin" in command:
        webbrowser.open("https://www.linkedin.com")

    elif "open github" in command:
        webbrowser.open("https://www.github.com")    

    elif command.startswith("play"):
        try:
            song = command.split(" ")[1]
            link = music_lib.music[song]
            webbrowser.open(link) 
        except (IndexError, KeyError):
            speak("Sorry, please specify a song from the music library.")

    elif "news" in command:
        news_api_key = os.environ.get("NEWS_API_KEY")
        if not news_api_key:
            speak("News API key is not configured. Please set it in the .env file.")
            return
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}")
    
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles',[])
            for article in articles:
                speak(article.get("title"))
    
    elif command.startswith("search for") or command.startswith("what is"):
        query = command.replace("search for", "").replace("what is", "").strip()
        
        try:
            speak(f"Searching Wikipedia for {query}")
            summary = wikipedia.summary(query, sentences=2)
            speak(f"According to Wikipedia: {summary}")

        except Exception:
            speak(f"Sorry, I couldn't find a Wikipedia page for {query}.")
            speak(f"I'll search Google for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")

    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")

    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {current_date}")



if __name__ == "__main__":
    speak("Hello, I am Loki, your personal assistant.") 

    while True:  
        print("Listening...")
    
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
                print("Recoginizing...")
                s_word = recognizer.recognize_google(audio)


            wakewords = ["lo ki", "loki", "hey loki"] 
            exitword = ["exit", "quit", "goodbye", "stop", "bye", "shut down"]
            if any(word in s_word.lower() for word in wakewords):
                print("How can I assist you?")
                speak("How can I assist you?")

                with sr.Microphone() as source:
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)
                    command_execution(command)
            
            elif any(word in s_word.lower() for word in exitword):
                speak("Goodbye! Have a great day.")
                exit()

    
        except sr.UnknownValueError:
            # When Google couldn't understand the audio
            print("Sorry, I didn't catch that. Could you please repeat?")
        except sr.RequestError:
            # When there's no internet connection or API issue
            print("My apologies, I'm having trouble connecting to the service.")
        except Exception as e:
            # For other errors, like the music library error you already handled
            print(f"An unexpected error occurred: {e}")
