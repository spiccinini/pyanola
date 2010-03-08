from model import Score, Note

def SSVParse(filename, resolution):
    g = open(filename)
    notes = []
    playing = [None] * 128
    for line in g:
        parts = line.split()
        delay = float(parts[0])*1000
        height = int(parts[1])
        speed = int(parts[2])
        if speed > 0:
            playing[height] = delay
        else:
            if playing[height] is not None:
                note = Note(playing[height], height, delay-playing[height])
                notes.append(note)
    return Score(notes, resolution)
