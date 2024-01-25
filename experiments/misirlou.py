import cv2
import mediapipe
import numpy
import rtmidi2
from rtmidi2 import CC
import time

"""Figuring out some stuff - test for track misirlou.
Created a visible note layout for right hand, it's more convenient to play, but it lacks versatility. 
User can play only one set of notes"""


# MIDI OUT Channel
CHANNEL_NUM = 2
# Tempo in sec
TEMPO = 0.03125


def adapt_chosen_notes_to_lines(value, number_of_lines):
    notes_preset = [66,65,68,69,71,72,75]
    scaled_value = notes_preset[number_of_lines - int(value * number_of_lines) -1]
    return numpy.round(scaled_value)


def send_notes(pitch=60, repeat=1):
    for note in range(repeat):
        midi_out.send_noteon(CHANNEL_NUM,pitch,80)
        time.sleep(TEMPO)
        midi_out.send_noteoff(CHANNEL_NUM,pitch)


midi_out = rtmidi2.MidiOut()
print(midi_out.ports)
midi_out.open_port(CHANNEL_NUM)


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
    h, w, c = img.shape
    number_of_lines = 7
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            index_x = hand_landmarks.landmark[mediapipeHands.HandLandmark.INDEX_FINGER_TIP].x
            index_y = hand_landmarks.landmark[mediapipeHands.HandLandmark.INDEX_FINGER_TIP].y
            if index_x * w >= 340:
                print("Right, midi notes ")
                v2 = adapt_chosen_notes_to_lines(index_y,number_of_lines)
                print(v2)
                send_notes(v2)
            mediapipeDraw.draw_landmarks(img, hand_landmarks,mediapipeHands.HAND_CONNECTIONS)

    fps = 1
    notes = ["E","F","G#","A","B","C","D#"]
    shift = 0
    for n in range(number_of_lines):
        img = cv2.line(img, (340, int(n*h/number_of_lines)), (w, int(n*h/number_of_lines)), (0, 255, 255))
        cv2.putText(img, notes[len(notes) - 1 - (n + shift) % len(notes)], (550, int((n+1)*h/number_of_lines) - 5), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)

    cv2.imshow("user", img)
    cv2.waitKey(fps)


