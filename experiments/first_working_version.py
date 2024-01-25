import cv2
import mediapipe
import numpy
import rtmidi2
from rtmidi2 import CC
import time
"""CC data(left hand) + MIDI notes(right hand) without any visible note layout.
Usable for playing some drone/ambient/noise music. Hard to play"""


# MIDI OUT Channel
CHANNEL_NUM = 2
# Tempo in sec
TEMPO = 0.125


def convert_range(value, in_min, in_max, out_min, out_max):
    l_span = in_max - in_min
    r_span = out_max - out_min
    scaled_value = (value - in_min) / l_span
    scaled_value = out_min + (scaled_value * r_span)
    return numpy.round(scaled_value)

def send_notes(pitch=60, repeat=1):
    for note in range(repeat):
        midiout.send_noteon(CHANNEL_NUM,pitch,80)
        time.sleep(TEMPO)
        midiout.send_noteoff(CHANNEL_NUM,pitch)

def send_mod(cc_chanel=CHANNEL_NUM, value=0):
    if value >= 0:
        midiout.send_cc(cc_chanel,75,value)


midiout = rtmidi2.MidiOut()
print(midiout.ports)
midiout.open_port(CHANNEL_NUM)


cap = cv2.VideoCapture(0)
mediapipeHands = mediapipe.solutions.hands
hands = mediapipeHands.Hands(static_image_mode=False,
                             max_num_hands=2,
                             min_detection_confidence=0.5,
                             min_tracking_confidence=0.5)
mediapipeDraw = mediapipe.solutions.drawing_utils

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # flipping img left2right
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # tweaking colors

    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        h, w, c = img.shape
        # print(results.multi_hand_landmarks)
        #
        #   !!! QUESTIONABLE APPROACH !!! left hand on the left side etc
        #       work in progress...
        #
        for hand_landmarks in results.multi_hand_landmarks:
            pink_x = hand_landmarks.landmark[mediapipeHands.HandLandmark.PINKY_TIP].x
            pink_y = hand_landmarks.landmark[mediapipeHands.HandLandmark.PINKY_TIP].y
            if pink_x * w < 340:
                print("Left, midi data")
                v1 = convert_range(pink_y, 1.0, 0.0, 0, 127)
                print(v1)
                send_mod(CHANNEL_NUM,v1)
            elif pink_x * w >= 340:
                print("Right, midi notes ")
                v2 = convert_range(pink_y, 1.0, -1.0, 60, 92)
                print(v2)
                send_notes(v2)
            mediapipeDraw.draw_landmarks(img, hand_landmarks,mediapipeHands.HAND_CONNECTIONS)

    fps = 1
    cv2.putText(img, str("Left: CC | Right: NOTES"), (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (50, 50, 50), 3)
    cv2.imshow("user", img)
    cv2.waitKey(fps)


