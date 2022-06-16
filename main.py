#Hello 1st commit

import speech_recognition as sr
from random import choice
import pyttsx3
import psutil
import requests
import os
from multiprocessing import Process


# Sign in to Wolfram Alpha and get API KEY/ APPID
APPID = "GA4XPU-9JGYA4XKYW"

responses = ['Yes boss', 'Yes sir', 'yes', 'what\'s up', 'I\'m here', 'I\'m listening', 'sir?']
exceptions = ['Try again sir', 'Is that English sir?', 'Could\'nt get that', 'Nothing, maybe the noise', 'Sorry sir, could not understand']
end_responses = ['Okay', 'Sure', 'I\'ll be here if you need me', 'Cool']


listener = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty("rate", 180)
voices = engine.getProperty("voices")
volume = engine.getProperty('volume')
engine.setProperty('volume', 1.0)
engine.setProperty("voice", voices[1].id)
voices = engine.getProperty("voices")
mic = sr.Microphone(device_index=1)



def AI(source):

        audio = listener.listen(source)
        try:
            user_input = listener.recognize_google(audio).lower()
            print(user_input)
            #"""Puts the machine to sleep"""
            if "sleep" == user_input:
                engine.say("Going to sleep")
                engine.runAndWait()
                os.system('rundll32.exe powrprof.dll,SetSuspendState Sleep')


            # """Control's who created the AI"""
            elif 'who created you' in user_input:
                engine.say("Jerrell Abrahams")
                engine.runAndWait()

            elif 'nothing' == user_input or 'nevermind' == user_input:
                engine.say(choice(end_responses))
                engine.runAndWait()

            # """Control's all what, why, how etc queries"""
            elif user_input:
                request = requests.get(f"http://api.wolframalpha.com/v1/spoken?appid={APPID}&i={user_input}")
                print(request.text)
                if request.text == "Wolfram Alpha did not understand your input":
                    engine.say(choice(exceptions))
                    engine.runAndWait()
                    return
                engine.say(request.text)
                engine.runAndWait()

        except Exception:
            engine.say("Something went wrong")
            listen()

def power_check():
    while True:
        battery = psutil.sensors_battery()
        if battery.power_plugged is False:
            engine.say("Power to machine has been lost!")
            engine.runAndWait()
            break

def listen():
    with mic as source:
        print("Listening...")
        listener.adjust_for_ambient_noise(source, duration=1)
        listener.dynamic_energy_threshold = False
        while True:

            try:
                audio = listener.listen(source)
                voice_text = listener.recognize_google(audio).lower()
                print(voice_text)
            except Exception:
                continue

            """Waits for call to start queries"""
            if "friday" in voice_text:
                engine.say(choice(responses))
                engine.runAndWait()
                AI(source)
                continue

            else:
                continue


if __name__ == '__main__':

    listen_process = Process(target=listen)
    listen_process.start()


    while True:
        """Checks if machine is charging"""
        if psutil.sensors_battery().power_plugged is True:
            power_check()