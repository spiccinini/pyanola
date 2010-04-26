import pyglet
from pyglet.window import key as K

class MapKeyToMidi(object):

    NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    MAP = {K.A:"C", K.S:"D", K.D:"E", K.F:"F", K.G:"G", K.H:"A",
           K.J:"B", K.K:"C", K.L:"D", K.W:"C#", K.E:"D#", 
           K.T:"F#", K.Y:"G#", K.U:"A#", K.O:"C#", K.P:"D#"}
    
    def __init__(self, octave=4):
        self.octave = octave

    def __call__(self, key):
        return self.key_to_midi(key)

    @classmethod
    def midi_note_int(cls, note, octave):
        return cls.NAMES.index(note) + 12 + 12 * int(octave)

    def key_to_midi(self, key):
        key_name = pyglet.window.key.symbol_string(key)
        if key_name == "CAPSLOCK":
            if self.octave < 8:
                self.octave += 0.5 # because its callen in note on and note off
        elif key_name == "LSHIFT":
            if self.octave > 0:
                self.octave -= 0.5
        
        midi_note_int = MapKeyToMidi.midi_note_int(self.MAP[key], self.octave)
        if key in [K.K, K.L, K.O, K.P]:
            midi_note_int += 12
        return midi_note_int
