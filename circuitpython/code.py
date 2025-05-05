import board
import displayio
import terminalio
from adafruit_display_text import label

display = board.DISPLAY
main_group = displayio.Group()
display.root_group = main_group

# Rensa allt
while len(main_group) > 0:
    main_group.pop()
display.refresh()

# Visa exakt det du vill
text = "Tjena"
text_area = label.Label(
    terminalio.FONT,
    text=text,
    color=0xFFFFFF,
    x=10,
    y=30,
    scale=2
)
main_group.append(text_area)
display.refresh()

# Håll igång loopen utan att göra något
while True:
    pass
