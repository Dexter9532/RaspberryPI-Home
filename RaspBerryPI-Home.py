import time
import os
import board
import busio
from adafruit_tca9548a import TCA9548A
from adafruit_neokey.neokey1x4 import NeoKey1x4

from vosk import Model, KaldiRecognizer
import sounddevice as sd
import json

# Skapa I2C-buss och initiera NeoKey
i2c = busio.I2C(board.SCL, board.SDA)
tca = TCA9548A(i2c)
neokey = NeoKey1x4(tca[0])

# Initiera Vosk-modellen
model = Model("/home/bobo/downloads/models/vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)

def speak(text):
    clean_text = text.strip().replace("\n", "").replace("\r", "") 
    print("Svarar:", clean_text)
    os.system(f'espeak "{clean_text}" 2>/dev/null')

def listen():
    print("Lyssnar...")
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1) as stream:
        while True:
            data = bytes(stream.read(4000)[0])
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result).get("text", "")
                return text.lower()

def show_display():
    try:
        with open("/dev/ttyACM0", "w") as serial:
            serial.write(f"Kommando: {command} | Svar: {response}\n")
    except Exception as e:
        print("Kunde inte skriva till ESP:", e)

while True:
    # Läser av alla knappar
    buttons = [neokey[i] for i in range(4)]

    # Hantera LED för alla knappar
    for i in range(4):
        if buttons[i]:
            neokey.pixels[i] = (255, 80, 0)  # Orange när nedtryckt
        else:
            neokey.pixels[i] = (0, 0, 0)

    # Idle Läge
    if buttons[0]:
        try:
            with open("/dev/ttyACM0", "w") as serial:
                serial.write("Hello Sir Bobo   RaspberryPi-Home By BoboINC\n")
        except Exception as e:
            print("Kunde inte skriva idle-text till ESP:", e)


    # Hantera taligenkänning via knapp 1
    if buttons[1]:
        print("Knapp 1 tryckt - lyssnar...")
        command = listen()
        print("Tolkad text:", command)

        if "date" in command:
            date = time.strftime("%A, %d %B")
            response = f"Today's date is: {date}"
            speak(response)
            show_display()

        elif "hello" in command:
            speak("Hello Sir Bobo")

        elif "working" in command:
            speak("Working perfectly!")


    # Knapp 2 = Avslutningsmeddelande
    if buttons[2]:
        speak("Goodbye Sir Bobo")
        time.sleep(1)

    time.sleep(0.5)
