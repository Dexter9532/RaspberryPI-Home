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
	if neokey[1]:
		print("Knapp 0 tryckt - lyssnar...")
        	command = listen()


        if "date" in command:
        	speak("Today's date is: " + command)

        elif "Hello" in command:
		speak("Hello Sir Bobo")

elif neokey[2]:
            speak("Working")

        neokey.pixels[1] = (255, 80, 0)

    else:
        neokey.pixels[1] = (0, 0, 0)

    time.sleep(0.1)
