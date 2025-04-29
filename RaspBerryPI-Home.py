import speech_recognition as sr
import time
import os
import board
import busio
from adafruit_tca9548a import TCA9548A
from adafruit_neokey.neokey1x4 import NeoKey1x4

# Skapa I2C-buss och initiera NeoKey
i2c = busio.I2C(board.SCL, board.SDA)
tca = TCA9548A(i2c)
neokey = NeoKey1x4(tca[0])

r = sr.Recognizer()

def speak(text):
    print("Svarar:", text)
    os.system(f'espeak "{text}"')

def listen():
    try:
        mic = sr.Microphone(device_index=2)  # Justera om nödvändigt
        with mic as source:
            print("Lyssnar...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

        text = r.recognize_google(audio, language="en-US")
        print("Du sa:", text)
        return text.lower()

    except (sr.UnknownValueError, sr.RequestError, AssertionError, AttributeError) as e:
        print(f"Fel vid lyssning: {e}")
        return ""

while True:
    # Läser av alla knappar
    buttons = [neokey[i] for i in range(4)]

    # Hantera LED för alla knappar
    for i in range(4):
        if buttons[i]:
            neokey.pixels[i] = (255, 80, 0)  # Exempel: orange när nedtryckt
        else:
            neokey.pixels[i] = (0, 0, 0)     # Släck LED annars

    # Nu kan vi hantera kommandon separat
    if buttons[1]:  # Knapp 1 tryckt
        print("Knapp 1 tryckt - lyssnar...")
        command = listen()

        if "date" in command:
            date = os.popen("date").read().strip()
            speak(f"Today's date is: {date}")

        elif "hello" in command:
            speak("Hello Sir Bobo")

        elif "working" in command:
            speak("Working perfectly!")

        time.sleep(1)  # Vänta lite så vi inte lyssnar flera gånger direkt

    if buttons[2]:  # Knapp 2 tryckt
        print("Knapp 2 tryckt - säger hejdå...")
        speak("Goodbye Sir Bobo")
        time.sleep(1)

    time.sleep(0.1)

