import datetime
import os
import subprocess
import sys
import time
import webbrowser
import psutil
import pyautogui
import pyttsx3
import speech_recognition as sr
import json
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import random
import numpy as np
# from elevenlabs import generate, play
# from elevenlabs import set_api_key
# from api_key import api_key_data
# set_api_key(api_key_data)

# def engine_talk(query):
#     audio = generate(
#         text=query, 
#         voice='Grace',
#         model="eleven_monolingual_v1"
#     )
#     play(audio)



with open("intents.json") as file:
    data = json.load(file)

model = load_model("chat_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer=pickle.load(f)

with open("label_encoder.pkl", "rb") as encoder_file:
    label_encoder=pickle.load(encoder_file)

def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 50)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume + 0.25)
    return engine

def speak(text):
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()

def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening........", end="", flush=True)
        r.pause_threshold = 1.0
        r.phrase_threshold = 0.3
        r.sample_rate = 48000
        r.dynamic_energy_threshold = True
        r.operation_timeout = 5
        r.non_speaking_duration = 0.5
        r.dynamic_energy_adjustment = 2
        r.energy_threshold = 4000
        r.phrase_time_limit = 10
        # print("Microphones available: ", sr.Microphone.list_microphone_names())
        audio = r.listen(source)
    try:
        print("\r", end="", flush=True)
        print("Recognizing....", end=" ", flush=True)
        query = r.recognize_google(audio, language='en-in')
        print("\r", end="", flush=True)
        print(f"User said: {query}\n")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return "None"
    except sr.UnknownValueError:
        print("Could not understand audio")
        return "None"
    except Exception as e:
        print(f"Error: {e}")
        return "None"
    return query

def cal_day():
    day = datetime.datetime.today().weekday() + 1
    day_dict = {
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
        7: "Sunday"
    }
    return day_dict.get(day, "Unknown Day")

def wishMe():
    hour = int(datetime.datetime.now().hour)
    t = time.strftime("%I:%M %p")
    day = cal_day()

    if hour >= 0 and hour < 12:
        speak(f"Good morning Ayush, it's {day} and the time is {t}")
    elif hour >= 12 and hour < 17:
        speak(f"Good evening Ayush, it's {day} and the time is {t}")
    else:
        speak(f"Good evening Ayush, it's {day} and the time is {t}")
    
def social_media(command):
        if 'facebook' in command:
            speak('opening facebook')
            webbrowser.open("https://www.facebook.com/")
        if 'discord' in command:
            speak('opening discord')
            webbrowser.open("https://discord.com/")
        if 'whatsapp' in command:
            speak('opening whatsapp')
            subprocess.run(["powershell", "-Command", "Start-Process shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App"], check=True)
        if 'instagram' in command:
            speak('opening instagram')
            webbrowser.open("https://www.instagram.com/")
        else:
            speak('no result found')

def schedule():
    day = cal_day()
    speak("Boss today's schedule is")
    week={
        "Monday": "clear",
        "Tuesday": "that you have Web Design and User Experience Engineering class from 6:10 pm to 9:40 pm",
        "Wednesday": "that you have co-op class from 11:45 am to 1:25 pm",
        "Thursday": "that you  have Application Engineering and Development class from 3:00 pm to 6:00 pm",
        "Friday": "clear",
        "Saturday": "that today you have a more relaxed day",
        "Sunday": " it's an holiday,but keep an eye on assignment deadlines",
    }
    if day in week.keys():
        speak(week[day])

def openApp(command):
    if "calc" in command:
        speak("opening calculator")
        os.startfile(r"C:\Windows\System32\calc.exe")
    elif "notepad" in command:
        speak("opening notepad")
        os.startfile(r"C:\Windows\System32\notepad.exe")


def CloseApp(command):
    if "calc" in command:
        speak("closing calculator")
        os.system('taskkill /f /im calc.exe')
    elif "notepad" in command:
        speak("closing notepad")
        os.system("taskkill /f /im notepad.exe")

def browsing(command):
    if 'open google' in command:
        speak("Boss, what should I search on google..")
        search_query = listen_command().lower()
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
    elif 'open edge' in command:
        speak("Boss, what should I search on edge..")
        search_query = listen_command().lower()
        webbrowser.open(f"https://www.bing.com/search?q={search_query}")

def condition():
    usage = str(psutil.cpu_percent())
    speak(f"CPU is at {usage} percentage")
    battery = psutil.sensors_battery()
    percentage = battery.percent
    speak(f"Boss our system have {percentage} percentage battery")

    if percentage>=80:
        speak("Boss we could have enough charging to continue our recording")
    elif percentage>=10 and percentage<=20:
        speak("Boss we should connect our system to charging point to charge our battery")
    else:
        speak("Boss we have very low power, please connect to charging otherwise recording should be off...")

    
    
if __name__ == "__main__":
    wishMe()
    # engine_talk("Allow me to introduce myself I am Jarvis, the virtual artificial intelligence and I'm here to assist you with a variety of tasks as best I can, 24 hours a day seven days a week.")

    while True:
        query = listen_command().lower()
        #query = input('Enter your command ->')
        if('facebook'in query) or ('discord' in query) or('whatsapp' in query)or('instagram' in query):
            social_media(query)
        elif('university time table' in query) or ('schedule' in query):
            schedule()
        elif ('volume up' in query) or ("increase volume" in query):
            pyautogui.press("volumeup")
            speak("Volume increased")
        elif ('volume down' in query) or ("decrease volume" in query):
            pyautogui.press("volumedown")
            speak("Volume decreased")
        elif ('volume mute' in query) or ("mute thw sound" in query):
            pyautogui.press("volumemute")
            speak("Volume muted")
        elif("open calc" in query) or ("open notepad" in query):
            openApp(query)
        elif("close calc" in query) or ("close notepad" in query):
            CloseApp(query)
        elif("what" in query) or ("who" in query) or("how" in query) or ("hi" in query) or("thanks" in query) or("hello" in query):
            padded_sequences = pad_sequences(tokenizer.texts_to_sequences([query]), maxlen=20, truncating='post')
            result = model.predict(padded_sequences)
            tag = label_encoder.inverse_transform([np.argmax(result)])
            for i in data['intents']:
                if i['tag'] == tag:
                    speak(np.random.choice(i['responses']))
        elif ("open google" in query) or ("edge" in query):
            browsing(query)
        elif ("system condition" in query) or ("condition of system" in query):
            speak("checking the system condition")
            condition()
        elif "exit" in query:
                    sys.exit()
    # speak("Hello, I'm JARVIS")
