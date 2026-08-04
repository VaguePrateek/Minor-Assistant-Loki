import music_lib
import requests
import wikipedia
import datetime
import re
import os
from dotenv import load_dotenv

load_dotenv()

exit_pattern = re.compile(r"\b(?:exit|quit|goodbye|stop|bye|shut down)\b", re.IGNORECASE)


def handle_command(command):
    command = command.lower().strip()
    responses = []
    url = None

    if not command:
        responses.append("Please say or type a command.")
    elif exit_pattern.search(command):
        responses.append("Goodbye! Have a great day.")
    elif "open youtube" in command:
        url = "https://www.youtube.com"
    elif "open google" in command:
        url = "https://www.google.com"
    elif "open instagram" in command:
        url = "https://instagram.com"
    elif "open facebook" in command:
        url = "https://www.facebook.com"
    elif "open linkedin" in command:
        url = "https://www.linkedin.com"
    elif "open github" in command:
        url = "https://www.github.com"
    elif command.startswith("play"):
        try:
            song = command.split(" ")[1]
            url = music_lib.music[song]
            responses.append(f"Playing {song} for you.")
        except (IndexError, KeyError):
            responses.append("Sorry, please specify a song from the music library.")
    elif "news" in command:
        news_api_key = os.environ.get("NEWS_API_KEY")
        if not news_api_key:
            responses.append("News API key is not configured. Please set it in the .env file.")
        else:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}")
            if r.status_code == 200:
                articles = r.json().get("articles", [])
                if not articles:
                    responses.append("No news headlines found right now.")
                for article in articles:
                    responses.append(article.get("title"))
            else:
                responses.append("Sorry, I couldn't fetch the news right now.")
    elif command.startswith("search for") or command.startswith("what is"):
        query = command.replace("search for", "").replace("what is", "").strip()
        responses.append(f"Searching Wikipedia for {query}.")
        try:
            summary = wikipedia.summary(query, sentences=2)
            responses.append(f"According to Wikipedia: {summary}")
        except Exception:
            responses.append(f"Sorry, I couldn't find a Wikipedia page for {query}. Opening a Google search instead.")
            url = f"https://www.google.com/search?q={query}"
    elif "time" in command:
        responses.append(f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}")
    elif "date" in command:
        responses.append(f"Today's date is {datetime.datetime.now().strftime('%B %d, %Y')}")
    else:
        responses.append("Sorry, I didn't understand that. Try 'open youtube', 'news', 'what is python', 'time' or 'date'.")

    return {"responses": responses, "url": url}
