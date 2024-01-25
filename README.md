<h1>SLEIGHT OF HAND APP</h1>
<h2>Python + OpenCV + Ableton</h2>
This app allows you to play music by moving your hands in front of a web camera.
<br>
It uses OpenCV library for hands tracking, transforms hands' movement to midi signals and sends them to Ableton Live.
<br>
<br>

Current version User decides on the number of notes he want to add to the screen layout, 
chooses the notes and preferred octaves from the table using a mouse.
Right side of the screen is divided for chosen number of parts and each part has the assigned note displayed on it.
By moving his index finger on the left side of the screen user sends Control Change data to the midi_out port
(For example, it can be used for controlling sound effects, or volume level in Ableton).
Movement of the index finger on the right side of the screen sends selected notes to the midi_out port.
