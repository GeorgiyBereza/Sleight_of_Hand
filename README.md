<h1>SLEIGHT OF HAND APP</h1>
<h2>Python + OpenCV + Ableton</h2>
<h3>  work in progress...</h3>
This app allows you to play music by moving your hands in front of a web camera.
<br>
It uses OpenCV library for hands tracking, transforms hands' movement to midi signals and sends them to Ableton Live.
<br>
<br>

In the current version User decides on the number of notes he want to add to the screen layout, 
chooses the notes and preferred octaves from the table using a mouse.
Right side of the screen is divided for chosen number of parts and each part has the assigned note displayed on it.
By moving his index finger on the left side of the screen user sends Control Change data to the midi_out port
(For example, it can be used for controlling sound effects, or volume level in Ableton).
Movement of the index finger on the right side of the screen sends selected notes to the midi_out port.

Ideas for further development:
<li>real GUI</li>
<li>functions for sending notes with preload presets:
like create your own layout of notes, or choose an octave, or choose a scale…</li>
<li>functions for sending cc signal: just signal from hand movement or modulation signal from set (sin, saw, square…) with amplitude controlled by hand</li>
<li>ability to choose a function for each hand from list of functions</li>
<li>working with separate midi_outs</li>
<li>tempo control</li>
<li>getting data through Ableton API</li>
<li>theremin setting?</li>

