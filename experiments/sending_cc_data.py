import sys
from scipy import signal
import time
import rtmidi2
import numpy as np
import matplotlib.pyplot as plt

"""Figuring out how to send control change data and how to deal with various modulation shapes"""

CHANNEL = 3
CC_NUM = 75
SPEED = 0.05

midiout = rtmidi2.MidiOut()
midiout.open_port(2)


def convert_range(value, in_min, in_max, out_min, out_max):
    l_span = in_max - in_min
    r_span = out_max - out_min
    scaled_value = (value - in_min) / l_span
    scaled_value = out_min + (scaled_value * r_span)
    return np.round(scaled_value)

def send_mod(amplitude,repeat):
    """Function which sends CC data to midi driver"""
    converted_amplitude = []
    for number in amplitude:
        result = convert_range(number, -1, 1, 0, 127)
        converted_amplitude.append(result)
    for _ in range(repeat):
        for val in converted_amplitude:
            midiout.send_cc(3,CC_NUM,val)
            time.sleep(SPEED)

def modulation_shape(shape: str, period: float, max_duration: float):
    """Function which shows a modulation shape"""
    x = np.arange(0,max_duration,0.01)

    if shape == 'sine':
        y = np.sin(2 * np.pi / period * x)
    elif shape == 'saw':
        y = signal.sawtooth(2 * np.pi / period * x)
    elif shape == 'square':
        y = signal.square(2 * np.pi / period * x)
    else:
        print('wrong type of wave')
        sys.exit()
    plt.plot(x, y)
    plt.ylabel(f"Amplitude = {shape} (time)")
    plt.xlabel("Time")
    plt.title('Modulation shape')
    plt.axhline(y=0, color='black')
    plt.show()
    return y


send_mod(modulation_shape('saw',1.0, 2.0),2)
midiout.close_port()
