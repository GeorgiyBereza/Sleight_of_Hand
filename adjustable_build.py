import cv2
import mediapipe
import numpy
import rtmidi2
import time

from choice_of_notes import notes_selection, enter_number_of_notes

"""This app allows you to play music by moving your hands in front of a web camera.
It uses OpenCV library for hands tracking, transforms movement to midi signals and sends them to Ableton Live.
In this version User decides on the number of notes he want to add to the screen layout
 and chooses the notes and preferred octaves from the table using a mouse.
 Right side of the screen is divided for chosen number of parts and each part has the assigned note displayed on it.
 By moving his index finger on the left side of the screen user sends Control Change data to the midi_out port
 (For example, it can be used for controlling some sound effect in Ableton).
 Movement of the index finger on the right side of the screen sends selected notes to the midi_out port"""



# default MIDI OUT Channel
CHANNEL_NUM = 2
# default tempo in seconds
TEMPO = 0.03125

midi_out = rtmidi2.MidiOut()
# NTS: to add an ability to change channels for output
# print(midi_out.ports)
midi_out.open_port(CHANNEL_NUM)


def send_notes(pitch=60, repeat=1):
    for note in range(repeat):
        midi_out.send_noteon(CHANNEL_NUM,pitch,80)
        time.sleep(TEMPO)
        midi_out.send_noteoff(CHANNEL_NUM,pitch)


def send_mod(cc_chanel=CHANNEL_NUM, value=0):
    if value >= 0:
        midi_out.send_cc(cc_chanel,75,value)


def convert_range(value, in_min, in_max, out_min, out_max):
    l_span = in_max - in_min
    r_span = out_max - out_min
    scaled_value = (value - in_min) / l_span
    scaled_value = out_min + (scaled_value * r_span)
    return numpy.round(scaled_value)


def adapt_chosen_notes_to_lines(value, number_of_notes, selected_notes_list):
    # notes_preset = [66,65,68,69,71,72,75]
    scaled_value = selected_notes_list[number_of_notes - int(value * number_of_notes) - 1]['midi_number']
    return numpy.round(scaled_value)


# User enters the desired number of notes and chooses them
NUMBER_OF_NOTES = enter_number_of_notes()
selected_notes = notes_selection(NUMBER_OF_NOTES)

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
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            index_x = hand_landmarks.landmark[mediapipeHands.HandLandmark.INDEX_FINGER_TIP].x
            index_y = hand_landmarks.landmark[mediapipeHands.HandLandmark.INDEX_FINGER_TIP].y
            if index_x * w < 340:
                print("Left, midi data")
                v1 = convert_range(index_y, 1.0, 0.0, 0, 127)
                print(v1)
                send_mod(CHANNEL_NUM, v1)
            elif index_x * w >= 340:
                print("Right, midi notes ")
                v2 = adapt_chosen_notes_to_lines(index_y, NUMBER_OF_NOTES, selected_notes)
                print(v2)
                send_notes(v2)
            mediapipeDraw.draw_landmarks(img, hand_landmarks,mediapipeHands.HAND_CONNECTIONS)

    fps = 1
    for n in range(NUMBER_OF_NOTES):
        img = cv2.line(img, (340, int(n*h/NUMBER_OF_NOTES)), (w, int(n*h/NUMBER_OF_NOTES)), (0, 255, 255))
        cv2.putText(img, selected_notes[NUMBER_OF_NOTES - n - 1]['note'],
                    (550, int((n+1)*h/NUMBER_OF_NOTES) - 5),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)

    cv2.imshow("Sleight of Hand", img)
    cv2.waitKey(fps)

