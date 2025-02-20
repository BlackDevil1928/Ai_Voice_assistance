# Import required libraries
from AppOpener import close, open as appopen 
from webbrowser import open as webopen 
from pywhatkit import search, playonyt 
from dotenv import dotenv_values 
from bs4 import BeautifulSoup  
from rich import print 
from groq import Groq
import webbrowser 
import subprocess
import requests 
import keyboard 
import asyncio 
import os  

env_vars = dotenv_values('.env')
GroqAPIKey = env_vars.get('GroqAPIKey')  # Retrieve the Groq API key.

classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta", 
           "IZ6rdc", "OSurRd LTKOO", "vLZv6d", "webanswers-webanswers_table__webanswers-table", "dDoNo ikb4Bb gsrt", "sXLaOe", 
           "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

client = Groq(api_key=GroqAPIKey)

professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need—don't hesitate to ask."
]

messages = []

SystemChatBot = [{'role': 'system', 'content': f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems etc."}]

def GoogleSearch(Topic):
    search(Topic)  # Use the search function to perform a Google search.
    return True  # Indicate success of the search.


def Content(Topic):
    # Nested function to open a file in Notepad.
    def OpenNotepad(File):
        default_text_editor = 'notepad.exe'  # Default text editor.
        subprocess.Popen([default_text_editor, File])

    # Nested function to generate content using the AI chatbot.
    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})  # Add the user's prompt to messages.

        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",  # Specify the AI model.
            messages=SystemChatBot + messages,  # Include system instructions and chat history.
            max_tokens=2048,  # Limit the response.
            temperature=0.7,  # Adjust response creativity.
            top_p=1,  # Use nucleus sampling for diversity.
            stream=True,  # Enable streaming of response chunks.
            stop=None  # Allow the model to continue stopping conditions.
        )

        Answer = "" 

        # Process streamed response chunks.
        for chunk in completion:
            if chunk.choices[0].delta.content:  # Check for content in the current chunk.
                Answer += chunk.choices[0].delta.content  # Append the content to the Answer.

        Answer = Answer.replace("</s>", "")  # Remove unwanted tokens from the response.
        messages.append({"role": "assistant", "content": Answer})  # Add the AI's response to messages.
        return Answer

    Topic: str = Topic.replace("Content ", "")  # Remove "Content " from the topic.
    ContentByAI = ContentWriterAI(Topic)  # Generate content using AI.

    # Save the generated content to a text file.
    with open(rf"Data/{Topic.lower().replace(' ', '')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI)  # Write the content to the file.
        file.close()

    OpenNotepad(rf"Data/{Topic.lower().replace(' ', '')}.txt")  # Open the file in Notepad.
    return True  # Indicate success.


# Function to search for a topic on YouTube.
def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"  # Construct the YouTube search URL.
    webbrowser.open(Url4Search)  # Open the search URL in a web browser.
    return True  # Indicate success.


def PlayYouTube(query):
    playonyt(query)  # Use pywhatkit's playonyt function to play the video.
    return True  # Indicate success.

def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True  # Indicate success.
    except Exception as e:
        print(f"Error opening app locally: {e}")

    try:
        query = f"{app}"  # Use the app name as the query.
        url = f"https://www.{query}.com"  # Create the URL in the desired format.
        
        # Open the constructed URL.
        webbrowser.open(url)
        return True
    except Exception as e:
        print(f"Error opening the webpage: {e}")
        return False

# OpenApp("canva")

# Function to close an application.
def CloseApp(app):
    if "chrome" in app:
        pass  # Skip if the app is Chrome.
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)  # Attempt to close the app.
            return True  # Indicate success.
        except:
            return False  # Indicate failure.


def System(command):
    # Nested function to mute the system volume.
    def mute():
        keyboard.press_and_release("volume mute")  # Simulate the mute key press.

    # Nested function to unmute the system volume.
    def unmute():
        keyboard.press_and_release("volume mute")  # Simulate the unmute key press.

    # Nested function to increase the system volume.
    def volume_up():
        keyboard.press_and_release("volume up")  # Simulate the volume up key press.

    # Nested function to decrease the system volume.
    def volume_down():
        keyboard.press_and_release("volume down")  # Simulate the volume down key press.

    # Execute the appropriate command.
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()

    return True  # Indicate success.

# Asynchronous function to translate and execute user commands.
async def TranslateAndExecute(commands: list[str]):

    funcs = []  # List to store asynchronous tasks.

    for command in commands:

        if command.startswith("open "):  # Handle "open" commands.

            if "open it" in command:  # Ignore "open it" commands.
                pass

            if "open file" == command:  # Ignore "open file" commands.
                pass

            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))  # Schedule app opening.
                funcs.append(fun)

        elif command.startswith("general "):  # Placeholder for general commands.
            pass

        elif command.startswith("realtime "):  # Placeholder for real-time commands.
            pass

        elif command.startswith("close "):  # Handle "close" commands.
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))  # Schedule app closing.
            funcs.append(fun)

        elif command.startswith("play "):  # Handle "play" commands.
            fun = asyncio.to_thread(PlayYouTube, command.removeprefix("play "))  # Schedule YouTube playback.
            funcs.append(fun)

        elif command.startswith("content "):  # Handle "content" commands.
            fun = asyncio.to_thread(Content, command.removeprefix("content "))  # Schedule content creation.
            funcs.append(fun)

        elif command.startswith("google search "):  # Handle Google search commands.
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))  # Schedule Google search.
            funcs.append(fun)

        elif command.startswith("youtube search "):  # Handle YouTube search commands.
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))  # Schedule YouTube search.
            funcs.append(fun)

        elif command.startswith("system "):  # Handle system commands.
            fun = asyncio.to_thread(System, command.removeprefix("system "))  # Schedule system command.
            funcs.append(fun)
        else:
            print(f"No Function Found. For {command}")  # Print an error for unrecognized commands.

    results = await asyncio.gather(*funcs)  # Execute all tasks concurrently.

    for result in results:  # Process the results.
        if isinstance(result, str):
            yield result
        else:
            yield result

async def Automation(commands: list[str]):

    async for result in TranslateAndExecute(commands):  # Translate and execute commands.
        pass

    return True  # Indicate success.
