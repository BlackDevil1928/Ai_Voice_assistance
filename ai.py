import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import pywhatkit
from googletrans import Translator


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


translator = Translator()

def speak(audio, lang="en"):
    """Convert text to speech."""
    engine.say(audio)   
    engine.runAndWait()

def wishMe():
    """Greet the user based on time of day."""
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("My name is Jonny, how may I help you?")

def takeCommand():
    """Recognize user speech and return translated text."""
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='auto') 
        print(f"User said: {query}")

       
        translated_text = translator.translate(query, dest="en").text
        print(f"Translated: {translated_text}")
        return translated_text.lower()

    except sr.UnknownValueError:
        print("Could not understand audio, please speak again.")
        return "None"
    
if __name__ == "__main__":
    speak("Hello")
    wishMe()
    
    while True:
        query = takeCommand()
        if query == "none":
            continue
        
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open instagram' in query:
            webbrowser.open("instagram.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'play music' in query:
            speak("What song would you like to play?")
            song = takeCommand()
            if song != "none":
                speak(f"Playing {song} on YouTube")
                pywhatkit.playonyt(song)

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif 'open vs code' in query:
            path = "C:\\Users\\laves\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(path)
