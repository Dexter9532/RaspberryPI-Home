import speech_recognition as sr
import time
import os

r = sr.Recognizer()

def speak(text):
    print("Svarar:", text)
    os.system(f'espeak "{text}"')

def listen():
    try:
        mic = sr.Microphone(device_index=2)  # OBS: justera index om det inte är 2

        with mic as source:
            print(" Lyssnar nu...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

        print(" Ljud fångat, tolkar...")
        text = r.recognize_google(audio, language="en-US")
        print(" Du sa:", text)
        return text.lower()

    except sr.UnknownValueError:
        print(" Kunde inte förstå.")
        return ""
    except sr.RequestError:
        print(" Nätverksfel.")
        return ""
    except AssertionError as e:
        print(f" Fel i mikrofonhantering: {e}")
        return ""
    except AttributeError as e:
        print(f" Mikrofonen verkar inte ge en ljudström: {e}")
        return ""

# Lyssnar hela tiden efter kommandon
while True:
    command = listen()

    if "time" in command or "what time is it" in command or "do you know the time" in command:
        now = time.strftime("%H:%M")
        speak(f"The time is {now}")

    elif "play sound" in command:
        os.system("aplay /home/bobo/projects/sound/test.wav")
        speak("Sound played.")

    elif "shutdown" in command:
        speak("Shutting down.")
        os.system("sudo shutdown now")

    else:
        print("Inget kommando hittades.")
