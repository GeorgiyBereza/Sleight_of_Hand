import tkinter as tk


class NotePickerApp:
    """This class creates the table of notes and octaves,
    user chooses desired notes for main screen by clicking on them"""

    def __init__(self, master, number_of_notes):
        self.master = master
        self.master.title("Note Picker")
        self.canvas = tk.Canvas(self.master, width=800, height=400, bg="white")
        self.canvas.pack()
        self.draw_note_table()
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.number_of_notes = number_of_notes
        self.selected_notes = []

    def draw_note_table(self):
        row_height = 30
        column_width = 60
        x_start = 10
        y_start = 10

        for midi_number in range(128):
            note = self.midi_to_note(midi_number)
            x = x_start + (midi_number % 12) * column_width
            y = y_start + (midi_number // 12) * row_height

            self.canvas.create_rectangle(x, y, x + column_width, y + row_height, fill="lightgray")
            self.canvas.create_text(x + column_width // 2, y + row_height // 2, text=note)

    def midi_to_note(self, midi_number):
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        note = note_names[midi_number % 12]
        octave = midi_number // 12 - 1  # Adjusted to start from octave -1
        return f"{note}{octave}"

    def on_canvas_click(self, event):
        x, y = event.x, event.y

        # Check which note was clicked
        for midi_number in range(128):
            note = self.midi_to_note(midi_number)
            x_start = (midi_number % 12) * 60 + 10
            y_start = (midi_number // 12) * 30 + 10
            x_end = x_start + 60
            y_end = y_start + 30

            if x_start <= x <= x_end and y_start <= y <= y_end:
                if len(self.selected_notes) < self.number_of_notes:
                    self.selected_notes.append({"note": note, "midi_number": midi_number})
                    print(f"Selected note: {note} (MIDI Number: {midi_number})")
                    if len(self.selected_notes) == self.number_of_notes:
                        print("Last note selected. Closing the application.")
                        self.master.destroy()
                else:
                    print("Maximum number of notes selected.")
                break


def enter_number_of_notes():
    while True:
        try:
            number_of_notes = int(input("Enter the number of notes to select: "))
            if number_of_notes >= 1:
                break
            else:
                print("Number should be >= 1")
        except:
            print("Try again")
    return number_of_notes



def notes_selection(number_of_notes):
    root = tk.Tk()
    note_picker = NotePickerApp(root, number_of_notes)
    root.lift()
    root.mainloop()

    # Displays the list of selected notes and their MIDI numbers
    # (ex. {'note': 'G6', 'midi_number': 91})
    print("\nList of selected notes:")
    for selected_note in note_picker.selected_notes:
        print(selected_note)
    return note_picker.selected_notes
