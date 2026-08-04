import speech_recognition as sr
import pyttsx3 as sx
import webbrowser
import re
from loki_core import handle_command

recognizer = sr.Recognizer()
engine = sx.init()


def speak(text):
    engine.say(text)
    engine.runAndWait()


if __name__ == "__main__":
    speak("Hello, I am Loki, your personal assistant.")

    wake_pattern = re.compile(r"\b(?:loki|lo ki|hey loki)\b", re.IGNORECASE)
    exit_pattern = re.compile(r"\b(?:exit|quit|goodbye|stop|bye|shut down)\b", re.IGNORECASE)

    while True:
        print("Listening...")

        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
                print("Recognizing...")
                spoken = recognizer.recognize_google(audio)

            if wake_pattern.search(spoken):
                print("How can I assist you?")
                speak("How can I assist you?")

                while True:
                    try:
                        with sr.Microphone() as source:
                            audio = recognizer.listen(source)
                            command = recognizer.recognize_google(audio)

                        if exit_pattern.search(command):
                            speak("Goodbye! Have a great day.")
                            exit()

                        result = handle_command(command)
                        for response in result["responses"]:
                            speak(response)
                        if result["url"]:
                            webbrowser.open(result["url"])
                        speak("Anything else?")

                    except sr.UnknownValueError:
                        print("Sorry, I didn't catch that. Could you please repeat?")
                        speak("Sorry, I didn't catch that. Could you please repeat?")
                    except sr.RequestError:
                        print("My apologies, I'm having trouble connecting to the service.")
                        speak("My apologies, I'm having trouble connecting to the service.")

            elif exit_pattern.search(spoken):
                speak("Goodbye! Have a great day.")
                exit()

        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Could you please repeat?")
        except sr.RequestError:
            print("My apologies, I'm having trouble connecting to the service.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
