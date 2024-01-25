import rtmidi2
import time
import random

"""Trying out sending random notes from 36 to 44 with pattern implemented with time.sleep"""

midi_out = rtmidi2.MidiOut()
ports = rtmidi2.get_out_ports()
print(ports)

midi_out.open_port(2)

x = 30
list = [2,2,1,10,2,2,1,1,1,1]
i = 0
while True:
    k = random.randint(0,10)
    if x > 44:
        x = 36
    else: x += k
    t = list[i%4]
    i += 1

    midi_out.send_noteon(3, x, 90)
    time.sleep(0.2)
    midi_out.send_noteon(3, x, 0)
    time.sleep(0.02*t)

