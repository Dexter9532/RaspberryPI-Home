import os
import board
import busio
from adafruit_tca9548a import TCA9548A
from adafruit_neokey.neokey1x4 import NeoKey1x4

# Skapa I2C-buss
i2c = busio.I2C(board.SCL, board.SDA)

# Initiera multiplexern
tca = TCA9548A(i2c)

# Välj kanal 0 där NeoKey är inkopplad
neokey = NeoKey1x4(tca[0])

print("Tryck på en knapp!")

while True:
    for i in range(4):
        if neokey[i]:
           print(f"Knapp {i} nedtryckt!")

           # Tänd LED på knapp i i grön färg
           neokey.pixels[i] = (255, 80, 0)

           if i == 0:
              print("Command 1 Speak")
              os.system("espeak 'Hello Sir' 2>/dev/null")

        else:
           # Släck LED när knappen släpps
           neokey.pixels[i] = (0, 0, 0)

    time.sleep(0.1)

