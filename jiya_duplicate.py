import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser
import smtplib
import pyaudio
import wikipedia
import tasks
import noisereduce as nr
import io
import requests
import soundfile as sf
import add_history
import jokes
import file_handel
from googletrans import Translator
import difflib
import mysql.connector


# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Store the conversation in this list
history = []

# DeepSeek API Key (Replace with your actual key)
DEEPSEEK_API_KEY = ""

# OpenWeatherMap API Key and URL
API_KEY = "your_openweathermap_api_key"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wish_me():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("Hello sir, What to do today")

def get_qa_data():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="jiya"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT question, answer FROM qa_data")
    data = {question.lower(): answer for question, answer in cursor.fetchall()}
    connection.close()
    return data

def get_best_match(question, qa_data):
    matches = difflib.get_close_matches(question, qa_data.keys(), n=1, cutoff=0.6)
    return qa_data[matches[0]] if matches else "I don't know the answer to that."

# Helper function to open websites
def open_website(url, label):
    speak(f"opening {label}")
    webbrowser.open(url)
    store_conversation(f"open {label}", f"Opening {label.capitalize()}.")

# Helper function to send email
def send_email(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    #server.login('bhattdev543@gmail.com', '11371137')
   # server.sendmail('devbhatt921@gmail.com', to, content)
    server.close()

def search_wikipedia(query):
    try:
        wikipedia.set_lang("en")
        summary = wikipedia.summary(query, sentences=2)
        speak(summary)
        store_conversation(query, summary)
    except Exception as e:
        speak("Sorry, I couldn't find any information on that topic.")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("I did not hear that, please say it again...")
        speak("I did not hear that, please say it again...")
        return "None"
    return query.lower()

def store_conversation(user_input, assistant_response):
    # Add conversation to the history
    history.append({'user_input': user_input, 'assistant_response': assistant_response})

# Function to fetch weather information
def get_weather(city):
    complete_url = f"{BASE_URL}q={city}&appid={API_KEY}&units=metric"  # Metric for Celsius
    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] == 200:
        main = data["main"]
        weather = data["weather"][0]
        temp = main["temp"]
        weather_desc = weather["description"]
        
        # Prepare the response
        weather_info = f"The temperature in {city} is {temp} degrees Celsius with {weather_desc}."
        return weather_info
    else:
        return "Sorry, I couldn't retrieve weather data. Please try again later."

def translate_text(text, target_language="en"):
    translator = Translator()
    translation = translator.translate(text,src='en', dest=target_language)
    translated_text = translation.text
    speak(f"The translation is: {translated_text}")
    return translated_text

def run():
    qa_data = get_qa_data()  # Fetch data from MySQL
    wish_me()
    task = tasks.remember()  # Assuming tasks.remember() exists and works
    speak("Today's Tasks are:")
    speak(task)

    while True:
        command = take_command()

        if not command:
            continue

        if 'None' in command:
            continue

        if 'open youtube' in command.lower():
            open_website("https://www.youtube.com", "youtube")
        
        elif 'open facebook' in command.lower():
            open_website("https://www.facebook.com", "facebook")
        
        elif 'open instagram' in command.lower():
            open_website("https://www.instagram.com", "instagram")

        elif 'open wikipedia' in command.lower():
            open_website("https://www.wikipedia.org", "instagram")
        
        elif 'open twitter' in command.lower() or 'open x' in command.lower():
            open_website("https://www.x.com", "twitter")
        
        elif 'open tiktok' in command.lower():
            open_website("https://www.tiktok.com", "tiktok")
        
        elif 'open google' in command.lower():
            open_website("https://www.google.com", "google")
        
        elif 'open bing' in command.lower():
            open_website("https://www.bing.com", "bing")
        
        elif 'open duckduckgo' in command.lower():
            open_website("https://www.duckduckgo.com", "duckduckgo")
        
        elif 'open bbc' in command.lower():
            open_website("https://www.bbc.com", "bbc")
        
        elif 'open cnn' in command.lower():
            open_website("https://www.cnn.com", "cnn")
        
        elif 'open nytimes' in command.lower():
            open_website("https://www.nytimes.com", "nytimes")
        
        elif 'open reddit' in command.lower():
            open_website("https://www.reddit.com", "reddit")
        
        elif 'open flipboard' in command.lower():
            open_website("https://www.flipboard.com", "flipboard")
        
        elif 'open gmail' in command.lower():
            open_website("https://mail.google.com", "gmail")
        
        elif 'open outlook' in command.lower():
            open_website("https://outlook.com", "outlook")
        
        elif 'open yahoo mail' in command.lower():
            open_website("https://mail.yahoo.com", "yahoo mail")
        
        elif 'open netflix' in command.lower():
            open_website("https://www.netflix.com", "netflix")
        
        elif 'open hulu' in command.lower():
            open_website("https://www.hulu.com", "hulu")
        
        elif 'open disney+' in command.lower():
            open_website("https://www.disneyplus.com", "disney+")
        
        elif 'open spotify' in command.lower():
            open_website("https://www.spotify.com", "spotify")
        
        elif 'open apple music' in command.lower():
            open_website("https://www.apple.com/apple-music/", "apple music")
        
        elif 'open amazon' in command.lower():
            open_website("https://www.amazon.com", "amazon")
        
        elif 'open ebay' in command.lower():
            open_website("https://www.ebay.com", "ebay")
        
        elif 'open etsy' in command.lower():
            open_website("https://www.etsy.com", "etsy")
        
        elif 'open aliexpress' in command.lower():
            open_website("https://www.aliexpress.com", "aliexpress")
        
        elif 'open wish' in command.lower():
            open_website("https://www.wish.com", "wish")
        
        elif 'open paypal' in command.lower():
            open_website("https://www.paypal.com", "paypal")
        
        elif 'open mint' in command.lower():
            open_website("https://www.mint.com", "mint")
        
        elif 'open personal capital' in command.lower():
            open_website("https://www.personalcapital.com", "personal capital")
        
        elif 'open chase' in command.lower():
            open_website("https://www.chase.com", "chase")
        
        elif 'open bank of america' in command.lower():
            open_website("https://www.bankofamerica.com", "bank of america")
        
        elif 'open google drive' in command.lower():
            open_website("https://drive.google.com", "google drive")
        
        elif 'open dropbox' in command.lower():
            open_website("https://www.dropbox.com", "dropbox")
        
        elif 'open slack' in command.lower():
            open_website("https://www.slack.com", "slack")
        
        elif 'open trello' in command.lower():
            open_website("https://www.trello.com", "trello")
        
        elif 'open asana' in command.lower():
            open_website("https://www.asana.com", "asana")
        
        elif 'open groupon' in command.lower():
            open_website("https://www.groupon.com", "groupon")
        
        elif 'open myfitnesspal' in command.lower():
            open_website("https://www.myfitnesspal.com", "myfitnesspal")
        
        elif 'open strava' in command.lower():
            open_website("https://www.strava.com", "strava")
        
        elif 'open weather.com' in command.lower():
            open_website("https://www.weather.com", "weather.com")
        
        elif 'open accuweather' in command.lower():
            open_website("https://www.accuweather.com", "accuweather")

        elif 'weather' in command.lower():
            city = command.split("weather in")[-1].strip()
            if city:
                weather_info = get_weather(city)
                speak(weather_info)
                store_conversation(command, weather_info)
            else:
                speak("Please specify the city after 'weather in'.")
                store_conversation(command, "User didn't specify city.")

        elif 'send email' in command:
            try:
                speak("What should I say?")
                content = take_command()
                to = "recipient_email@gmail.com"
                send_email(to, content)
                speak("Email has been sent.")
                store_conversation(command, f"Sent email to {to} with content: {content}")
            except Exception as e:
                speak("Sorry, I could not send the email.")
                store_conversation(command, "Failed to send email.")

        elif 'wikipedia' in command:
            search_wikipedia(command)
            store_conversation(command,"Wikipeadia")

        elif 'time' in command:
            speak(f"The time is {datetime.datetime.now().strftime('%H:%M')}")
            store_conversation(command, "Responded with the current time.")

        elif 'tell me joke' in command:
            joke=jokes.get_random_joke()
            speak(joke)

        # Command to create a file
        elif 'create a file' in command:
            speak("What should be the name of the file?")
            filename = take_command()
            speak("What content do you want to write in the file?")
            content = take_command()
            output=file_handel.create_file(filename, content)
            speak(output)
        
        # Command to read a file
        elif 'read the file' in command:
            speak("Which file do you want me to read?")
            filename = take_command()
            output=file_handel.read_file(filename)
            speak(output)
        
        # Command to append content to a file
        elif 'append to the file' in command:
            speak("Which file do you want to append to?")
            filename = take_command()
            speak("What content do you want to add?")
            content = take_command()
            output=file_handel.append_to_file(filename, content)
            speak(output)
        
        # Command to delete a file
        elif 'delete the file' in command:
            speak("Which file do you want to delete?")
            filename = take_command()
            output=file_handel.delete_file(filename)
            speak(output)

        elif 'translate' in command:
            speak("What text would you like to translate?")
            text_to_translate = take_command()  # Get the text to translate
            
            if text_to_translate:
                speak("What language do you want to translate to? (e.g., en for English, fr for French)")
                target_language = take_command()  # Get the target language
                target_language=target_language[-2:]
                
                if target_language:
                    translate_text(text_to_translate, target_language)
                    store_conversation(command, f"Translated '{text_to_translate}' to {target_language}")
                else:
                    speak("I didn't catch the target language. Please try again.")
                    store_conversation(command, "Target language not specified.")
                    
            else:
                speak("I didn't catch the text to translate. Please try again.")
                store_conversation(command, "Text not provided for translation.")

        elif 'quit' in command:
            speak("Goodbye!")
            add_history.store_conversations_in_db(history,uid)  # Store entire conversation history to the database
            return 2
            break

        else:
            answer = get_best_match(command, qa_data)
            speak(answer)
